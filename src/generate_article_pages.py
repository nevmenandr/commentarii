#!/usr/bin/env python3
"""
generate_article_pages.py

Генерирует HTML-обёртки для статей TEI-издания
«Commentarii Academiae Scientiarum Imperialis Petropolitanae: Editio Digitalis».

Каждая HTML-обёртка:
- подключает CETEI.js и style.css;
- загружает соответствующий TEI-XML из ../../xml/tomus1/;
- отображает статью через CETEIcean.

Использование:
    python3 src/generate_article_pages.py

Скрипт читает список статей из ARTICLES (ниже) и создаёт
по одному HTML-файлу на каждую в папке docs/articles/.

Скрипт предполагает такую структуру репозитория:

    commentarii/
    ├── src/
    │   └── generate_article_pages.py   ← этот файл
    ├── xml/
    │   └── tomus1/
    │       ├── tomus1.xml
    │       ├── tomus1_titulus.xml
    │       └── ...
    └── docs/
        ├── index.html
        ├── catalogue.html
        ├── style.css
        ├── CETEI.js
        └── articles/                    ← сюда пишутся HTML-обёртки

Пути указаны относительно корня репозитория (а не относительно
расположения скрипта), поэтому запускать скрипт нужно из корня:

    cd commentarii
    python3 src/generate_article_pages.py
"""

from pathlib import Path
from string import Template


# ---------------------------------------------------------------------------
# Настройки путей
# ---------------------------------------------------------------------------
# Пути отсчитываются от корня репозитория.
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent   # .../commentarii
OUTPUT_DIR = REPO_ROOT / "docs" / "articles" / "tomus1"          # docs/articles/

# Пути внутри HTML-файлов (относительно docs/articles/*.html)
XML_RELATIVE_PATH = "../../xml/tomus1"   # → commentarii/xml/tomus1/
CSS_RELATIVE_PATH = "../../style.css"      # → docs/style.css
JS_RELATIVE_PATH = "../../CETEI.js"         # → docs/CETEI.js


# ---------------------------------------------------------------------------
# Список статей
# ---------------------------------------------------------------------------
# Каждый элемент — словарь с полями:
#   file      — имя XML-файла без расширения (совпадает с именем HTML-файла)
#   title_ru  — название статьи по-русски (для <title> в HTML)
#   title_la  — название статьи по-латыни (для <h1> в шапке страницы)
#   author    — автор (по-русски, опционально)
#   section   — раздел, к которому относится статья (для якоря в оглавлении)
#
# Порядок соответствует оглавлению тома (catalogue.html).
# ---------------------------------------------------------------------------

ARTICLES = [
    # --- Начальные материалы ---
    {
        "file": "tomus1_titulus",
        "title_ru": "Титульный лист",
        "title_la": "Titulus Tomi I",
        "author": "",
        "section": "front",
    },
    {
        "file": "tomus1_dedicatio",
        "title_ru": "Посвящение Петру II",
        "title_la": "Dedicatio Petro II",
        "author": "Христиан Гольдбах",
        "section": "front",
    },
    {
        "file": "tomus1_praefatio",
        "title_ru": "Предисловие",
        "title_la": "Praefatio",
        "author": "Христиан Гольдбах",
        "section": "front",
    },
    {
        "file": "tomus1_index",
        "title_ru": "Оглавление тома",
        "title_la": "Index Commentariorum",
        "author": "",
        "section": "front",
    },

    # --- Classis Prima continens Mathematica ---
    {
        "file": "tomus1_classis1_titulus",
        "title_ru": "Титульный лист раздела Mathematica",
        "title_la": "Titulus Classis Primae",
        "author": "",
        "section": "mathesis",
    },
    {
        "file": "hermann_de_mensura_virium",
        "title_ru": "О мере сил тел",
        "title_la": "De Mensura virium Corporum",
        "author": "Якоб Герман",
        "section": "mathesis",
    },
    {
        "file": "bulfinger_de_viribus_corpori_moto",
        "title_ru": "О силах, присущих движущемуся телу, и их мере",
        "title_la": "De Viribus corpori moto insitis et illarum Mensura",
        "author": "Георг Бернхард Бюльфингер",
        "section": "mathesis",
    },
    {
        "file": "bernoulli_de_motu_corporum_ex_percussione",
        "title_ru": "О движении тел от удара",
        "title_la": "De Motu corporum ex percussione",
        "author": "Николай Бернулли",
        "section": "mathesis",
    },
    {
        "file": "bernoulli_examen_principiorum",
        "title_ru": "Исследование начал механики",
        "title_la": "Examen Principiorum Mechanicae",
        "author": "Даниил Бернулли",
        "section": "mathesis",
    },
    {
        "file": "hermann_de_problemate_kepleriano",
        "title_ru": "О задаче Кеплера",
        "title_la": "De Problemate Kepleriano",
        "author": "Якоб Герман",
        "section": "mathesis",
    },
    {
        "file": "hermann_de_calculo_integrali",
        "title_ru": "Об интегральном исчислении",
        "title_la": "De Calculo Integrali",
        "author": "Якоб Герман",
        "section": "mathesis",
    },
    {
        "file": "bernoulli_de_integrationibus",
        "title_ru": "Об интегрировании дифференциальных уравнений",
        "title_la": "De Integrationibus Aequationum Differentialium",
        "author": "Иоганн Бернулли",
        "section": "mathesis",
    },
    {
        "file": "goldbach_de_casibus_integrabilibus",
        "title_ru": "О некоторых случаях интегрируемости",
        "title_la": "De Casibus quibusdam integrabilibus",
        "author": "Христиан Гольдбах",
        "section": "mathesis",
    },
    {
        "file": "bernoulli_analysis_aequationum",
        "title_ru": "Анализ некоторых дифференциальных уравнений",
        "title_la": "Analysis Aequationum quarundam Differentialium",
        "author": "Николай Бернулли",
        "section": "mathesis",
    },
    {
        "file": "goldbach_methodus_integrandi",
        "title_ru": "Метод интегрирования дифференциального уравнения",
        "title_la": "Methodus integrandi Aequationem differentialem",
        "author": "Христиан Гольдбах",
        "section": "mathesis",
    },
    {
        "file": "hermann_de_epicycloidibus",
        "title_ru": "О сферических эпициклоидах",
        "title_la": "De Epicycloidibus Sphaericis",
        "author": "Якоб Герман",
        "section": "mathesis",
    },
    {
        "file": "wolff_principia_dynamica",
        "title_ru": "Начала динамики",
        "title_la": "Principia Dynamica",
        "author": "Христиан Вольф",
        "section": "mathesis",
    },

    # --- Classis Secunda continens Physica ---
    {
        "file": "tomus1_classis2_titulus",
        "title_ru": "Титульный лист раздела Physica",
        "title_la": "Titulus Classis Secundae",
        "author": "",
        "section": "physica",
    },
    {
        "file": "buxbaum_nova_plantarum_genera",
        "title_ru": "Новые роды растений",
        "title_la": "Nova Plantarum genera",
        "author": "Иоганн Христиан Буксбаум",
        "section": "physica",
    },
    {
        "file": "bulfinger_de_directione_corporum",
        "title_ru": "О направлении тяжёлых тел в сферическом вихре",
        "title_la": "De directione Corporum gravium in vortice Sphaerico",
        "author": "Георг Бернхард Бюльфингер",
        "section": "physica",
    },
    {
        "file": "duvernoi_descriptio_vasorum",
        "title_ru": "Описание млечных сосудов",
        "title_la": "Descriptio Vasorum Chyliferorum",
        "author": "Иоганн Георг Дю Вернуа",
        "section": "physica",
    },
    {
        "file": "bernoulli_tentamen_novae",
        "title_ru": "Опыт новой теории движения мышц",
        "title_la": "Tentamen novae de motu Musculorum Theoriae",
        "author": "Даниил Бернулли",
        "section": "physica",
    },
    {
        "file": "bernoulli_experimentum_circa_neruum",
        "title_ru": "Эксперимент относительно зрительного нерва",
        "title_la": "Experimentum circa nervum opticum",
        "author": "Даниил Бернулли",
        "section": "physica",
    },
    {
        "file": "bulfinger_de_variis_barometris",
        "title_ru": "О различных более чувствительных барометрах",
        "title_la": "De variis Barometris sensibilibus",
        "author": "Георг Бернхард Бюльфингер",
        "section": "physica",
    },
    {
        "file": "duvernoi_de_cisterna",
        "title_ru": "О грудном протоке кашалота, тюленя и слона",
        "title_la": "De Cisterna et ductu Thoracico Catopardi, Phocae et Elephanti",
        "author": "Иоганн Георг Дю Вернуа",
        "section": "physica",
    },
    {
        "file": "meyer_de_luce_boreali",
        "title_ru": "О северном сиянии",
        "title_la": "De Luce Boreali",
        "author": "Фридрих Христофор Мейер",
        "section": "physica",
    },
    {
        "file": "michelotti_rari_morbi_historia",
        "title_ru": "История редкой и почти неслыханной болезни матки",
        "title_la": "Rari ac prope inauditi ex utero morbi historia",
        "author": "Пётр Антоний Микелотти",
        "section": "physica",
    },
    {
        "file": "observationes_anatomicae",
        "title_ru": "Анатомические наблюдения",
        "title_la": "Observationes Anatomicae",
        "author": "",
        "section": "physica",
    },

    # --- Classis Tertia continens Historica et Critica ---
    {
        "file": "tomus1_classis3_titulus",
        "title_ru": "Титульный лист раздела Historica et Critica",
        "title_la": "Titulus Classis Tertiae",
        "author": "",
        "section": "historia",
    },
    {
        "file": "bayer_de_origine_scytharum",
        "title_ru": "О происхождении и древних местах обитания скифов",
        "title_la": "De origine et priscis sedibus Scytharum",
        "author": "Теофил Сигфрид Байер",
        "section": "historia",
    },
    {
        "file": "bayer_de_situ_scythiae",
        "title_ru": "О положении Скифии во времена Геродота",
        "title_la": "De situ Scythiae sub aetatem Herodoti",
        "author": "Теофил Сигфрид Байер",
        "section": "historia",
    },
    {
        "file": "bayer_de_muro_caucaseo",
        "title_ru": "О Кавказской стене",
        "title_la": "De Muro Caucaseo",
        "author": "Теофил Сигфрид Байер",
        "section": "historia",
    },

    # --- Observationes Astronomicae Petropoli factae ---
    {
        "file": "tomus1_observationes_titulus",
        "title_ru": "Титульный лист раздела астрономических наблюдений",
        "title_la": "Titulus Observationum Astronomicarum",
        "author": "",
        "section": "astronomia",
    },
    {
        "file": "lisle_observationes_astronomicae",
        "title_ru": "Астрономические наблюдения",
        "title_la": "Observationes Astronomicae",
        "author": "Иосиф Николай Делиль и Людовик Делиль де ла Круайер",
        "section": "astronomia",
    },
]


# ---------------------------------------------------------------------------
# Шаблон HTML
# ---------------------------------------------------------------------------

HTML_TEMPLATE = Template("""\
<!doctype html>
<html lang="la">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$title_la — Commentarii Academiae Scientiarum Imperialis Petropolitanae</title>
  <link rel="stylesheet" href="$css_path" />
  <script src="$js_path"></script>
</head>
<body>

<header>
  <p class="breadcrumb">
    <a href="../../index.html">Главная</a> ·
    <a href="../../catalogue.html">Оглавление Тома I</a>
  </p>
  <h1>$title_la</h1>
  <p class="subtitle">$title_ru</p>
  <p class="author">$author</p>
</header>

<main>
  <div id="TEI"></div>
</main>

<footer>
  <p>
    <a href="https://github.com/nevmenandr/commentarii">Репозиторий на GitHub</a> ·
    CC BY 4.0
  </p>
</footer>

<script>
  (function () {
    var CETEIcean = new CETEI();
    CETEIcean.getHTML5("$xml_path/$file.xml", function (data) {
      document.getElementById("TEI").appendChild(data);
    });
  })();
</script>

</body>
</html>
""")


# ---------------------------------------------------------------------------
# Генерация
# ---------------------------------------------------------------------------

def generate_pages() -> None:
    """Создаёт по одному HTML-файлу на каждую статью из ARTICLES."""

    # Создаём выходную папку, если её нет
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for article in ARTICLES:
        file_base = article["file"]
        html_path = OUTPUT_DIR / f"{file_base}.html"

        html_content = HTML_TEMPLATE.substitute(
            title_la=article.get("title_la", ""),
            title_ru=article.get("title_ru", ""),
            author=article.get("author", ""),
            file=file_base,
            xml_path=XML_RELATIVE_PATH,
            css_path=CSS_RELATIVE_PATH,
            js_path=JS_RELATIVE_PATH,
        )

        html_path.write_text(html_content, encoding="utf-8")
        print(f"  создан: {html_path.relative_to(REPO_ROOT)}")

    # Подсчитываем распределение по разделам
    sections = {}
    for article in ARTICLES:
        s = article.get("section", "other")
        sections[s] = sections.get(s, 0) + 1

    print()
    print(f"Всего сгенерировано файлов: {len(ARTICLES)}")
    print()
    print("Распределение по разделам:")
    for s, count in sorted(sections.items()):
        print(f"  {s}: {count}")
    print()
    print(f"Папка: {OUTPUT_DIR.relative_to(REPO_ROOT)}")


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Генерация HTML-обёрток для статей...")
    print()
    generate_pages()
