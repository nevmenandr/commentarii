#!/usr/bin/env python3
"""
validate_tei.py

Валидация TEI-файлов по схеме (RelaxNG или XSD).

Использование:
    python3 src/validate_tei.py                      # проверить все XML в xml/
    python3 src/validate_tei.py xml/tomus1/          # проверить конкретную папку
    python3 src/validate_tei.py --schema schema/tei.rng
    python3 src/validate_tei.py --schema schema/tei.xsd

Схема ищется в таком порядке:
    1. Путь, указанный в --schema.
    2. schema/tei.rng
    3. schema/tei.xsd
    4. schema/tei_all.rng (скачанная схема TEI All)

Если схема не найдена, скрипт проверяет только well-formedness XML.

Зависимости:
    pip install lxml
"""

import argparse
import sys
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    print("Ошибка: требуется библиотека lxml. Установите:")
    print("  pip install lxml")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Настройки по умолчанию
# ---------------------------------------------------------------------------

DEFAULT_XML_DIR = Path("xml")
SCHEMA_CANDIDATES = [
    Path("schema/tei.rng"),
    Path("schema/tei.xsd"),
    Path("schema/tei_all.rng"),
    Path("schema/tei_all.xsd"),
]


# ---------------------------------------------------------------------------
# Поиск схемы
# ---------------------------------------------------------------------------

def find_schema(explicit_path: Path | None) -> Path | None:
    """Возвращает путь к схеме или None, если схема не найдена."""
    if explicit_path:
        if explicit_path.is_file():
            return explicit_path
        print(f"Ошибка: указанная схема не найдена: {explicit_path}")
        sys.exit(1)

    for candidate in SCHEMA_CANDIDATES:
        if candidate.is_file():
            return candidate

    return None


# ---------------------------------------------------------------------------
# Загрузка схемы
# ---------------------------------------------------------------------------

def load_relaxng(schema_path: Path):
    """Загружает RelaxNG-схему."""
    return etree.RelaxNG(etree.parse(str(schema_path)))


def load_xsd(schema_path: Path):
    """Загружает XSD-схему."""
    return etree.XMLSchema(etree.parse(str(schema_path)))


def load_schema(schema_path: Path):
    """Определяет тип схемы по расширению и загружает её."""
    suffix = schema_path.suffix.lower()
    if suffix == ".rng":
        return load_relaxng(schema_path)
    elif suffix == ".xsd":
        return load_xsd(schema_path)
    else:
        print(f"Ошибка: неизвестный формат схемы: {suffix}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Валидация одного файла
# ---------------------------------------------------------------------------

def validate_file(xml_path: Path, schema) -> bool:
    """Возвращает True, если файл валиден, иначе False."""
    try:
        doc = etree.parse(str(xml_path))
    except etree.XMLSyntaxError as e:
        print(f"  ✗ {xml_path}")
        print(f"    Ошибка разбора XML: {e}")
        return False

    if schema is None:
        # Только well-formedness
        print(f"  ✓ {xml_path} (well-formed)")
        return True

    if schema.validate(doc):
        print(f"  ✓ {xml_path}")
        return True
    else:
        print(f"  ✗ {xml_path}")
        for error in schema.error_log:
            print(f"    Строка {error.line}: {error.message}")
        return False


# ---------------------------------------------------------------------------
# Сбор XML-файлов
# ---------------------------------------------------------------------------

def collect_xml_files(root: Path) -> list[Path]:
    """Рекурсивно собирает все .xml файлы в папке."""
    if root.is_file():
        return [root] if root.suffix.lower() == ".xml" else []
    return sorted(root.rglob("*.xml"))


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Валидация TEI-файлов по схеме."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=str(DEFAULT_XML_DIR),
        help="Файл или папка с XML для валидации (по умолчанию: xml/)",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=None,
        help="Путь к схеме RelaxNG или XSD.",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"Ошибка: путь не существует: {target}")
        sys.exit(1)

    schema_path = find_schema(args.schema)
    if schema_path:
        print(f"Схема: {schema_path}")
        schema = load_schema(schema_path)
    else:
        print("Схема не найдена. Проверка только well-formedness XML.")
        schema = None

    files = collect_xml_files(target)
    if not files:
        print(f"XML-файлы не найдены в: {target}")
        sys.exit(0)

    print(f"Найдено файлов: {len(files)}")
    print()

    valid = 0
    invalid = 0
    for xml_path in files:
        if validate_file(xml_path, schema):
            valid += 1
        else:
            invalid += 1

    print()
    print(f"Валидных:   {valid}")
    print(f"Невалидных: {invalid}")

    sys.exit(0 if invalid == 0 else 1)


if __name__ == "__main__":
    main()
