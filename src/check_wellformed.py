#!/usr/bin/env python3
"""
check_wellformed.py

Быстрая проверка well-formedness XML-файлов (без схемы).

Использование:
    python3 src/check_wellformed.py                # проверить xml/
    python3 src/check_wellformed.py xml/tomus1/    # проверить папку
    python3 src/check_wellformed.py path/file.xml  # проверить один файл

Зависимости:
    нет (используется стандартный xml.etree.ElementTree)

Возвращает код 0, если все файлы well-formed, иначе 1.
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


# ---------------------------------------------------------------------------
# Настройки по умолчанию
# ---------------------------------------------------------------------------

DEFAULT_XML_DIR = Path("xml")


# ---------------------------------------------------------------------------
# Сбор XML-файлов
# ---------------------------------------------------------------------------

def collect_xml_files(root: Path) -> list[Path]:
    """Рекурсивно собирает все .xml файлы в папке."""
    if root.is_file():
        return [root] if root.suffix.lower() == ".xml" else []
    return sorted(root.rglob("*.xml"))


# ---------------------------------------------------------------------------
# Проверка одного файла
# ---------------------------------------------------------------------------

def check_file(xml_path: Path) -> tuple[bool, str]:
    """
    Возвращает (True, "") если файл well-formed,
    иначе (False, "сообщение об ошибке").
    """
    try:
        ET.parse(str(xml_path))
        return True, ""
    except ET.ParseError as e:
        return False, str(e)
    except OSError as e:
        return False, f"Ошибка чтения файла: {e}"


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Проверка well-formedness XML-файлов."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=str(DEFAULT_XML_DIR),
        help="Файл или папка с XML (по умолчанию: xml/)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Выводить только ошибки.",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"Ошибка: путь не существует: {target}")
        sys.exit(1)

    files = collect_xml_files(target)
    if not files:
        print(f"XML-файлы не найдены в: {target}")
        sys.exit(0)

    if not args.quiet:
        print(f"Найдено файлов: {len(files)}")
        print()

    valid = 0
    invalid = 0
    for xml_path in files:
        ok, error = check_file(xml_path)
        if ok:
            valid += 1
            if not args.quiet:
                print(f"  ✓ {xml_path}")
        else:
            invalid += 1
            print(f"  ✗ {xml_path}")
            print(f"    {error}")

    if not args.quiet:
        print()
        print(f"Well-formed:   {valid}")
        print(f"С ошибками:    {invalid}")

    sys.exit(0 if invalid == 0 else 1)


if __name__ == "__main__":
    main()
