#!/usr/bin/env python3
"""
stats.py

Подсчёт статистики по TEI-файлам издания:
- количество файлов;
- количество статей;
- количество абзацев, заголовков, формул, рисунков;
- количество ссылок на рисунки;
- количество слов;
- количество персоналий, организаций, мест;
- распределение по классификаторам (<textClass>).

Использование:
    python3 src/stats.py                    # статистика по xml/
    python3 src/stats.py xml/tomus1/        # по конкретной папке
    python3 src/stats.py --json             # вывод в JSON

Зависимости:
    pip install lxml
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    print("Ошибка: требуется библиотека lxml. Установите:")
    print("  pip install lxml")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Настройки
# ---------------------------------------------------------------------------

DEFAULT_XML_DIR = Path("xml")
TEI_NS = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI_NS}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


# ---------------------------------------------------------------------------
# Сбор XML-файлов
# ---------------------------------------------------------------------------

def collect_xml_files(root: Path) -> list[Path]:
    """Рекурсивно собирает все .xml файлы в папке."""
    if root.is_file():
        return [root] if root.suffix.lower() == ".xml" else []
    return sorted(root.rglob("*.xml"))


# ---------------------------------------------------------------------------
# Сбор статистики по одному файлу
# ---------------------------------------------------------------------------

def count_words(tree) -> int:
    """
    Считает количество слов в тексте: собирает весь текст
    из <tei:p> и <tei:head>, разбивает по пробелам.
    """
    text_parts = []
    for el in tree.iter(f"{{{TEI_NS}}}p", f"{{{TEI_NS}}}head"):
        # Собираем текст, исключая служебные элементы
        text = "".join(el.itertext())
        text_parts.append(text)
    full_text = " ".join(text_parts)
    words = [w for w in full_text.split() if any(c.isalpha() for c in w)]
    return len(words)


def collect_file_stats(tree) -> dict:
    """Собирает статистику по одному файлу."""
    stats = {
        "paragraphs": 0,
        "heads": 0,
        "formulas": 0,
        "figures": 0,
        "figure_refs": 0,
        "notes": 0,
        "persNames": 0,
        "orgNames": 0,
        "placeNames": 0,
        "titles": 0,
        "dates": 0,
        "refs": 0,
        "words": 0,
        "textClass": None,
    }

    stats["paragraphs"] = len(tree.findall(f".//{{{TEI_NS}}}p"))
    stats["heads"] = len(tree.findall(f".//{{{TEI_NS}}}head"))
    stats["formulas"] = len(tree.findall(f".//{{{TEI_NS}}}formula"))
    stats["figures"] = len(tree.findall(f".//{{{TEI_NS}}}figure"))
    stats["notes"] = len(tree.findall(f".//{{{TEI_NS}}}note"))
    stats["persNames"] = len(tree.findall(f".//{{{TEI_NS}}}persName"))
    stats["orgNames"] = len(tree.findall(f".//{{{TEI_NS}}}orgName"))
    stats["placeNames"] = len(tree.findall(f".//{{{TEI_NS}}}placeName"))
    stats["titles"] = len(tree.findall(f".//{{{TEI_NS}}}title"))
    stats["dates"] = len(tree.findall(f".//{{{TEI_NS}}}date"))

    for ref in tree.findall(f".//{{{TEI_NS}}}ref"):
        stats["refs"] += 1
        if ref.get("type") == "figure":
            stats["figure_refs"] += 1

    stats["words"] = count_words(tree)

    # Классификатор (например, mathesis, physica, historia)
    class_code = tree.find(f".//{{{TEI_NS}}}classCode")
    if class_code is not None and class_code.text:
        stats["textClass"] = class_code.text.strip()

    return stats


# ---------------------------------------------------------------------------
# Сбор общей статистики
# ---------------------------------------------------------------------------

def collect_stats(files: list[Path]) -> dict:
    """Собирает статистику по всем файлам."""
    totals = Counter()
    class_counter = Counter()
    articles = []

    for xml_path in files:
        try:
            tree = etree.parse(str(xml_path))
        except etree.XMLSyntaxError as e:
            print(f"  ✗ {xml_path}: ошибка разбора: {e}")
            continue

        file_stats = collect_file_stats(tree)
        file_stats["file"] = xml_path.name

        for key, value in file_stats.items():
            if key in ("file", "textClass"):
                continue
            if isinstance(value, int):
                totals[key] += value

        if file_stats["textClass"]:
            class_counter[file_stats["textClass"]] += 1
            articles.append({
                "file": xml_path.name,
                "class": file_stats["textClass"],
                "words": file_stats["words"],
            })

    totals["files"] = len(files)
    totals["articles"] = len(articles)

    return {
        "totals": dict(totals),
        "classes": dict(class_counter),
        "articles": articles,
    }


# ---------------------------------------------------------------------------
# Вывод
# ---------------------------------------------------------------------------

def print_report(result: dict) -> None:
    """Печатает статистику в читаемом виде."""
    totals = result["totals"]
    classes = result["classes"]

    print("=" * 60)
    print("Статистика издания")
    print("=" * 60)
    print()

    print("Общее:")
    print(f"  Всего XML-файлов:      {totals.get('files', 0)}")
    print(f"  Статей (с textClass):  {totals.get('articles', 0)}")
    print(f"  Слов:                  {totals.get('words', 0)}")
    print()

    print("Структура текста:")
    print(f"  Абзацев (<p>):         {totals.get('paragraphs', 0)}")
    print(f"  Заголовков (<head>):   {totals.get('heads', 0)}")
    print(f"  Примечаний (<note>):   {totals.get('notes', 0)}")
    print()

    print("Формулы и рисунки:")
    print(f"  Формул (<formula>):    {totals.get('formulas', 0)}")
    print(f"  Рисунков (<figure>):   {totals.get('figures', 0)}")
    print(f"  Ссылок на рисунки:     {totals.get('figure_refs', 0)}")
    print()

    print("Именованные сущности:")
    print(f"  Персоналии:            {totals.get('persNames', 0)}")
    print(f"  Организации:           {totals.get('orgNames', 0)}")
    print(f"  Места:                 {totals.get('placeNames', 0)}")
    print(f"  Названия:              {totals.get('titles', 0)}")
    print(f"  Даты:                  {totals.get('dates', 0)}")
    print(f"  Ссылки (<ref>):        {totals.get('refs', 0)}")
    print()

    if classes:
        print("Распределение по классам:")
        for class_name, count in sorted(classes.items()):
            print(f"  {class_name}: {count}")
        print()


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Статистика по TEI-файлам издания."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=str(DEFAULT_XML_DIR),
        help="Файл или папка с XML (по умолчанию: xml/)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Выводить в формате JSON.",
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

    result = collect_stats(files)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
