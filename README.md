[![TEI P5](https://img.shields.io/badge/TEI-P5-blue.svg)](https://tei-c.org/) [![18th Century](https://img.shields.io/badge/18th-century-purple.svg)](https://en.wikipedia.org/wiki/18th_century) [![Language: Latin](https://img.shields.io/badge/Language-Latin-yellow.svg)](https://en.wikipedia.org/wiki/Latin) [![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

# Commentarii Academiae Scientiarum Imperialis Petropolitanae: Editio Digitalis

Электронное научное издание «Записки Императорской Санкт-Петербургской академии наук: Цифровое издание».

![cover](images/index.jpeg)

## О проекте

*Commentarii Academiae Scientiarum Imperialis Petropolitanae* — научный журнал, издававшийся Императорской Санкт-Петербургской академией наук с 1728 года. В журнале публиковались статьи по математике, физике, астрономии, анатомии, естественной истории, истории и т. п.

Настоящее электронное издание представляет собой цифровую публикацию томов журнала. В издание включаются **только тексты на латинском языке**; статьи на других языках (немецком, французском и др.) в издание не входят.

Тексты транскрибированы, исправлены от ошибок OCR, размечены в формате TEI P5 и снабжены метаданными, пригодными для машинной обработки и научного цитирования.

## Источники

Сканы томов взяты из открытых цифровых коллекций:

- **Internet Archive** — основной источник PDF-файлов (например, [Том I](https://archive.org/download/commentariiacade01impe/commentariiacade01impe_bw.pdf)).
- **British Museum (Natural History), Лондон** — экземпляр, с которого сделан скан Тома I.

Каждый том в издании снабжён ссылкой на источник в `<sourceDesc>`.

## Принципы транскрипции

- Ошибки OCR исправлены; исправления не отмечаются в тексте, но оригинальные написания могут быть восстановлены по сканам.
- Лигатуры (например, `CIƆ IƆ` для дат, `æ`, `œ`) раскрыты в тексте.
- Разночтения и спорные места документируются в `<note>`.

## Формат и стандарты

- **TEI P5** (Text Encoding Initiative) — основной формат разметки.
- Каждый документ — автономный `<TEI>`-файл с собственным `<teiHeader>`.
- Контейнеры `commentarii.xml` и `tomus1.xml` связывают документы через **XInclude**.
- Кодировка — **UTF-8**.
- Метаданные включают автора, название, источник, язык, лицензию и сведения об издателе.

## Состав издания

### Том I (1728)

- Титульный лист
- Посвящение Петру II (Христиан Гольдбах)
- Предисловие (Христиан Гольдбах)

Последующие тома добавляются по мере обработки.

## Структура репозитория

```
commentarii/
├── README.md
├── LICENSE
├── CITATION.cff
├── xml/
│   ├── commentarii.xml          # Контейнер всего издания
│   ├── tomus1/
│   │   ├── tomus1.xml           # Контейнер Тома I
│   │   ├── tomus1_titulus.xml   # Титульный лист
│   │   ├── tomus1_dedicatio.xml # Посвящение
│   │   ├── tomus1_praefatio.xml # Предисловие
│   │   └── ...                  # Статьи Тома I
│   └── ...
├── images/
│   └── tomus1/                  # Изображения со страниц
└── docs/                        # GitHub Pages
```

## Участие и обратная связь

Если вы нашли ошибку в транскрипции или хотите предложить улучшение — создайте issue в [репозитории](https://github.com/nevmenandr/commentarii) или напишите редактору.

## Лицензия

Издание распространяется на условиях лицензии **Creative Commons Attribution 4.0 International (CC BY 4.0)**. Вы можете свободно использовать, распространять и адаптировать материалы при условии указания авторства.

## Цитирование

Если вы используете это издание в научной работе, пожалуйста, ссылайтесь на него следующим образом:

```
Орехов, Борис. Commentarii Academiae Scientiarum Imperialis Petropolitanae: Editio Digitalis. 2026. URL: https://github.com/nevmenandr/commentarii
```

Машиночитаемая информация для цитирования доступна в файле [`CITATION.cff`](CITATION.cff).


## Аннотация

### Русский

Электронное научное издание «Записки Императорской Санкт-Петербургской академии наук: Цифровое издание» представляет собой цифровую публикацию томов научного журнала *Commentarii Academiae Scientiarum Imperialis Petropolitanae*, издававшегося Императорской Санкт-Петербургской академией наук с 1728 года. В издание включаются только тексты на латинском языке — статьи по математике, физике, астрономии, анатомии, естественной истории и истории. Тексты транскрибированы, исправлены от ошибок OCR и размечены в формате TEI P5.

### English

A digital edition of the *Commentarii Academiae Scientiarum Imperialis Petropolitanae*, the proceedings of the Imperial St. Petersburg Academy of Sciences, originally published in the 18th century. The edition includes only Latin texts — articles on mathematics, physics, astronomy, anatomy, natural history, and history. The texts are transcribed, corrected from OCR errors, and encoded in TEI P5.

### Latina

Editio digitalis *Commentariorum Academiae Scientiarum Imperialis Petropolitanae*, actorum Academiae Scientiarum Imperialis Petropolitanae, saeculo duodevicesimo editorum. Haec editio solos textus Latinos complectitur — commentarios de mathesi, physica, astronomia, anatomia, historia naturali atque historia. Textus transcripti, erroribus OCR purgati, et in forma TEI P5 expressi sunt.

## Контакты

[Борис Орехов / Boris Nuceus / Boris Orekhov](https://nevmenandr.github.io/): 

[![Bluesky](https://img.shields.io/badge/Bluesky-0285FF?style=for-the-badge&logo=Bluesky&logoColor=white)](https://bsky.app/profile/nevmenandr.bsky.social) [![Mastodon](https://img.shields.io/badge/-MASTODON-%232B90D9?style=for-the-badge&logo=mastodon&logoColor=white)](https://mastodon.social/@nevmenandr) [![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/schonenrede) [![X](https://img.shields.io/badge/X-%23000000.svg?style=for-the-badge&logo=X&logoColor=white)](https://x.com/nevmenandr) [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/@schonenrede/)

[![academia Logo](https://img.shields.io/badge/academia-41454A?style=flat-square&logo=academia&logoColor=white)](https://hse-ru.academia.edu/BorisOrekhov) [![arxiv Logo](https://img.shields.io/badge/-arxiv-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/search/cs?searchtype=author&query=Orekhov,+B) [![dev.to Logo](https://img.shields.io/badge/dev-000000?style=flat-square&logo=dev.to&logoColor=white)](https://dev.to/nevmenandr) [![elsevier Logo](https://img.shields.io/badge/elsevier-FF6C00?style=flat-square&logo=elsevier&logoColor=white)](https://www.scopus.com/authid/detail.uri?authorId=57190401804) [![habr Logo](https://img.shields.io/badge/habr-65A3BE?style=flat-square&logo=habr&logoColor=white)](https://habr.com/ru/users/nevmenandr/) [![huggingface Logo](https://img.shields.io/badge/huggingface-FFD21E?style=flat-square&logo=huggingface&logoColor=white)](https://huggingface.co/nevmenandr) [![orcid Logo](https://img.shields.io/badge/orcid-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0000-0002-9099-0436) [![osf Logo](https://img.shields.io/badge/osf-2CB9F1?style=flat-square&logo=osf&logoColor=white)](https://osf.io/phy74/) 

[![pypi Logo](https://img.shields.io/badge/pypi-3775A9?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/user/nevmenandr/) [![researchgate Logo](https://img.shields.io/badge/researchgate-00CCBB?style=flat-square&logo=researchgate&logoColor=white)](https://researchgate.net/profile/Boris-Orekhov) [![semanticscholar Logo](https://img.shields.io/badge/semanticscholar-1857B6?style=flat-square&logo=semanticscholar&logoColor=white)](https://www.semanticscholar.org/author/Boris-V.-Orekhov/2080424505)  [![wikipedia Logo](https://img.shields.io/badge/wikipedia-000000?style=flat-square&logo=wikipedia&logoColor=white)](https://ru.wikipedia.org/wiki/%D0%A3%D1%87%D0%B0%D1%81%D1%82%D0%BD%D0%B8%D0%BA:Nevmenandr)


