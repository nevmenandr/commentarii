#!/usr/bin/env python3
"""
check_refs.py

Проверка внутренних ссылок в TEI-файлах:
- все <ref target="#xyz"> должны указывать на существующий xml:id="xyz";
- все xml:id в документе должны быть уникальны;
- все <ref type="figure" target="#fig..."> должны указывать на существующий <figure>.

По умолчанию проверка ведётся в пределах одного документа.
С флагом --cross-file проверяются ссылки между всеми файлами в папке
(полезно, если в будущем появятся кросс-документные ссылки).

Использование:
    python3 src/check_refs.py                    # проверить xml/
    python3 src/check_refs.py xml/tomus1/
    python3 src/check_refs.py --cross-file xml/tomus1/

Зависимости:
    pip install lxml
"""

import argparse
import sys
from collections import defaultdict
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
TEI_NS = "http://www.tei-c.org/ns/1.0"


# ---------------------------------------------------------------------------
# Сбор XML-файлов
# ---------------------------------------------------------------------------

def collect_xml_files(root: Path) -> list[Path]:
    """Рекурсивно собирает все .xml файлы в папке."""
    if root.is_file():
        return [root] if root.suffix.lower() == ".xml" else []
    return sorted(root.rglob("*.xml"))


# ---------------------------------------------------------------------------
# Извлечение xml:id и ссылок
# ---------------------------------------------------------------------------

def get_xml_ids(tree) -> dict[str, list[int]]:
    """
    Возвращает словарь {xml_id: [строки, где встречается]}.
    Если id повторяется, в списке будет несколько строк.
    """
    ids: dict[str, list[int]] = defaultdict(list)
    for el in tree.iter():
        xml_id = el.get("{http://www.w3.org/XML/1998/namespace}id")
        if xml_id:
            ids[xml_id].append(el.sourceline or 0)
    return ids


def get_refs(tree) -> list[tuple[str, int]]:
    """
    Возвращает список ссылок (target, строка) для всех <ref target="#...">.
    """
    refs = []
    for el in tree.iter(f"{{{TEI_NS}}}ref"):
        target = el.get("target")
        if target and target.startswith("#"):
            refs.append((target[1:], el.sourceline or 0))
    return refs


def get_figure_ids(tree) -> set[str]:
    """Возвращает множество xml:id всех <figure>."""
    figure_ids = set()
    for el in tree.iter(f"{{{TEI_NS}}}figure"):
        xml_id = el.get("{http://www.w3.org/XML/1998/namespace}id")
        if xml_id:
            figure_ids.add(xml_id)
    return figure_ids


def get_figure_refs(tree) -> list[tuple[str, int]]:
    """Возвращает список ссылок на рисунки (<ref type="figure" target="#...">)."""
    refs = []
    for el in tree.iter(f"{{{TEI_NS}}}ref"):
        if el.get("type") == "figure":
            target = el.get("target")
            if target and target.startswith("#"):
                refs.append((target[1:], el.sourceline or 0))
    return refs


# ---------------------------------------------------------------------------
# Проверка одного файла
# ---------------------------------------------------------------------------

def check_file(xml_path: Path) -> dict:
    """Проверяет один файл. Возвращает словарь с результатами."""
    try:
        tree = etree.parse(str(xml_path))
    except etree.XMLSyntaxError as e:
        return {
            "path": xml_path,
            "error": f"Ошибка разбора XML: {e}",
            "duplicate_ids": {},
            "missing_refs": [],
            "missing_figure_refs": [],
        }

    ids = get_xml_ids(tree)
    refs = get_refs(tree)
    figure_ids = get_figure_ids(tree)
    figure_refs = get_figure_refs(tree)

    # Дубликаты xml:id
    duplicate_ids = {i: lines for i, lines in ids.items() if len(lines) > 1}

    # Битые ссылки
    missing_refs = [(target, line) for target, line in refs if target not in ids]

    # Битые ссылки на рисунки
    missing_figure_refs = [
        (target, line) for target, line in figure_refs if target not in figure_ids
    ]

    return {
        "path": xml_path,
        "error": None,
        "duplicate_ids": duplicate_ids,
        "missing_refs": missing_refs,
        "missing_figure_refs": missing_figure_refs,
    }


# ---------------------------------------------------------------------------
# Кросс-файловая проверка
# ---------------------------------------------------------------------------

def check_cross_file(files: list[Path]) -> dict:
    """
    Собирает все xml:id из всех файлов и проверяет,
    что каждая ссылка находится хотя бы в одном файле.
    """
    all_ids: dict[str, list[Path]] = defaultdict(list)

    for xml_path in files:
        try:
            tree = etree.parse(str(xml_path))
        except etree.XMLSyntaxError:
            continue
        for xml_id in get_xml_ids(tree):
            all_ids[xml_id].append(xml_path)

    # Проверяем ссылки
    broken: list[tuple[Path, str, int]] = []
    duplicates: dict[str, list[Path]] = {}

    for xml_id, paths in all_ids.items():
        if len(paths) > 1:
            duplicates[xml_id] = paths

    for xml_path in files:
        try:
            tree = etree.parse(str(xml_path))
        except etree.XMLSyntaxError:
            continue
        for target, line in get_refs(tree):
            if target not in all_ids:
                broken.append((xml_path, target, line))

    return {
        "broken": broken,
        "duplicates": duplicates,
    }


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Проверка внутренних ссылок в TEI-файлах."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=str(DEFAULT_XML_DIR),
        help="Файл или папка с XML для проверки (по умолчанию: xml/)",
    )
    parser.add_argument(
        "--cross-file",
        action="store_true",
        help="Проверять ссылки между всеми файлами в папке.",
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

    print(f"Найдено файлов: {len(files)}")
    print()

    if args.cross_file:
        # Кросс-файловая проверка
        print("Режим: кросс-файловая проверка")
        print()
        result = check_cross_file(files)

        if result["duplicates"]:
            print("Дубликаты xml:id между файлами:")
            for xml_id, paths in result["duplicates"].items():
                print(f"  {xml_id}:")
                for p in paths:
                    print(f"    {p}")
            print()

        if result["broken"]:
            print("Битые ссылки:")
            for xml_path, target, line in result["broken"]:
                print(f"  {xml_path}:{line}  →  #{target}")
            print()

        if not result["duplicates"] and not result["broken"]:
            print("Все ссылки корректны.")
            sys.exit(0)
        else:
            sys.exit(1)

    else:
        # Проверка в пределах каждого файла
        print("Режим: проверка в пределах каждого файла")
        print()
        total_errors = 0

        for xml_path in files:
            result = check_file(xml_path)

            if result["error"]:
                print(f"  ✗ {xml_path}")
                print(f"    {result['error']}")
                total_errors += 1
                continue

            has_errors = (
                result["duplicate_ids"]
                or result["missing_refs"]
                or result["missing_figure_refs"]
            )

            if not has_errors:
                print(f"  ✓ {xml_path}")
                continue

            print(f"  ✗ {xml_path}")

            if result["duplicate_ids"]:
                print("    Дубликаты xml:id:")
                for xml_id, lines in result["duplicate_ids"].items():
                    print(f"      {xml_id}: строки {lines}")

            if result["missing_refs"]:
                print("    Битые ссылки:")
                for target, line in result["missing_refs"]:
                    print(f"      строка {line}  →  #{target}")

            if result["missing_figure_refs"]:
                print("    Битые ссылки на рисунки:")
                for target, line in result["missing_figure_refs"]:
                    print(f"      строка {line}  →  #{target}")

            total_errors += 1

        print()
        if total_errors:
            print(f"Файлов с ошибками: {total_errors}")
            sys.exit(1)
        else:
            print("Все файлы корректны.")
            sys.exit(0)


if __name__ == "__main__":
    main()
