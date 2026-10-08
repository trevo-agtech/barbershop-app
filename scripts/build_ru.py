#!/usr/bin/env python3
"""Build /ru pages from English sources + patch ES/EN for RU hreflang/switcher."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://barbershopvalencia.es"

PAGE_MAP = {
    "index.html": "index.html",
    "el-carmen.html": "el-carmen.html",
    "la-petxina.html": "la-petxina.html",
    "services.html": "services.html",
    "contact.html": "contact.html",
}

# Longer phrases first
RU_FROM_EN: list[tuple[str, str]] = [
    ("Barber Shop Valencia | Barbershop in Valencia · El Carmen & La Petxina",
     "Barber Shop Valencia | Барбершоп в Валенсии · El Carmen и La Petxina"),
    ("Barber Shop Valencia — barbershop in Valencia for men. Two shops: El Carmen (C/ Baja 50) and La Petxina (C/ Juan Llorens 18). Barbers near you, cuts, beard and easy booking.",
     "Barber Shop Valencia — барбершоп в Валенсии для мужчин. Два салона: El Carmen (C/ Baja 50) и La Petxina (C/ Juan Llorens 18). Барберы рядом, стрижки, борода и запись онлайн."),
    ("Barber Shop Valencia | Barbershop in Valencia",
     "Barber Shop Valencia | Барбершоп в Валенсии"),
    ("Valencia barbershop in El Carmen and La Petxina. Book your haircut or beard.",
     "Барбершоп в Валенсии: El Carmen и La Petxina. Запишитесь на стрижку или бороду."),
    ("Barber Shop Valencia El Carmen | Barbershop on C/ Baja 50",
     "Barber Shop Valencia El Carmen | Барбершоп на C/ Baja 50"),
    ("Barber Shop Valencia El Carmen: barbershop in Valencia on C/ Baja 50. Men’s cuts, fades and beard. Book on Booksy or WhatsApp.",
     "Barber Shop Valencia El Carmen: барбершоп в Валенсии на C/ Baja 50. Мужские стрижки, фейды и борода. Запись через Booksy или WhatsApp."),
    ("Barber Shop Valencia El Carmen on C/ Baja 50. Book your cut or beard.",
     "Barber Shop Valencia El Carmen на C/ Baja 50. Запишитесь на стрижку или бороду."),
    ("La Petxina Barbershop Valencia | Barber Shop Valencia, Juan Llorens 18",
     "Барбершоп La Petxina Валенсия | Barber Shop Valencia, Juan Llorens 18"),
    ("Barber Shop Valencia in La Petxina: barbershop in Valencia at C/ Juan Llorens 18. Men’s cuts, beard and treatments. Book on Booksy or WhatsApp.",
     "Barber Shop Valencia в La Petxina: барбершоп в Валенсии на C/ Juan Llorens 18. Мужские стрижки, борода и уходы. Запись через Booksy или WhatsApp."),
    ("Barbershop in Valencia · La Petxina, C/ Juan Llorens 18. Book your cut or beard.",
     "Барбершоп в Валенсии · La Petxina, C/ Juan Llorens 18. Запишитесь на стрижку или бороду."),
    ("Services & prices | Barbershop Valencia · Barber Shop Valencia",
     "Услуги и цены | Барбершоп Валенсия · Barber Shop Valencia"),
    ("Men’s barbershop menu in Valencia: cuts, beard and treatments at El Carmen and La Petxina. Prices and booking at Barber Shop Valencia.",
     "Меню барбершопа для мужчин в Валенсии: стрижки, борода и уходы в El Carmen и La Petxina. Цены и запись в Barber Shop Valencia."),
    ("Services & prices | Barber Shop Valencia",
     "Услуги и цены | Barber Shop Valencia"),
    ("Barbershop services in Valencia at El Carmen and La Petxina. Book by shop.",
     "Услуги барбершопа в Валенсии в El Carmen и La Petxina. Запись по салону."),
    ("Contact | Barber Shop Valencia · Barbers near you",
     "Контакты | Barber Shop Valencia · Барберы рядом"),
    ("Contact Barber Shop Valencia: WhatsApp +34 677 142 958. Barbershop in Valencia at El Carmen and La Petxina. Barbers near you for cut or beard.",
     "Свяжитесь с Barber Shop Valencia: WhatsApp +34 677 142 958. Барбершоп в Валенсии — El Carmen и La Petxina. Барберы рядом для стрижки или бороды."),
    ("Contact | Barber Shop Valencia",
     "Контакты | Barber Shop Valencia"),
    ("Barbers near you in Valencia. El Carmen and La Petxina.",
     "Барберы рядом в Валенсии. El Carmen и La Petxina."),
    ("Two barbershops in Valencia. Haircuts, beard work and men’s grooming with a team that minds the details.",
     "Два барбершопа в Валенсии. Стрижки, борода и мужской уход с командой, которая следит за деталями."),
    ("Two shops in Valencia. A clean cut, a defined beard and a team that minds the details.",
     "Два салона в Валенсии. Чистая стрижка, чёткая борода и команда, которая ценит детали."),
    ("Precise cuts. Current style.", "Точные стрижки. Актуальный стиль."),
    ("Each shop has its own menu. Book directly at the location you prefer.",
     "У каждого салона своё меню. Запишитесь напрямую в удобный локал."),
    ("Same hours at El Carmen and La Petxina. Public holidays may vary.",
     "Одинаковый график в El Carmen и La Petxina. В праздники возможны изменения."),
    ("Barber products we use in the chair: pomades, razors, clippers and skincare.",
     "Продукты для барбершопа, которые мы используем: помады, бритвы, машинки и уход за кожей."),
    ("Choose a shop. Each one has its own menu and booking link.",
     "Выберите салон. У каждого своё меню и ссылка для записи."),
    ("Style and barbershop tips in Valencia",
     "Стиль и советы барбершопа в Валенсии"),
    ("Haircut, beard and booking tips. The latest articles from Barber Shop Valencia.",
     "Советы по стрижкам, бороде и записи. Последние статьи Barber Shop Valencia."),
    ("Two shops, expert barbers and online booking.",
     "Два салона, опытные барберы и онлайн-запись."),
    ("Barbershop appointments in Valencia",
     "Барбершоп с записью в Валенсии"),
    ("Book online and arrive on time — no waiting.",
     "Запишитесь онлайн и приходите вовремя — без очереди."),
    ("See all blog posts", "Смотреть весь блог"),
    ("9 October in Valencia: La Petxina open",
     "9 октября в Валенсии: La Petxina открыта"),
    ("Nou d’Octubre holiday: what to do, celebration cuts and booking at La Petxina. El Carmen closed.",
     "Праздник Nou d’Octubre: чем заняться, стрижки к празднику и запись в La Petxina. El Carmen закрыт."),
    ("Barbershop in Valencia: men's style and professional service",
     "Барбершоп в Валенсии: мужской стиль и профессиональный сервис"),
    ("Interior of Barber Shop Valencia El Carmen", "Интерьер Barber Shop Valencia El Carmen"),
    ("Interior of Barber Shop Valencia", "Интерьер Barber Shop Valencia"),
    ("Storefront of Barber Shop Valencia El Carmen", "Фасад Barber Shop Valencia El Carmen"),
    ("Haircut at Barber Shop Valencia", "Стрижка в Barber Shop Valencia"),
    ("Scissor detail at Barber Shop Valencia", "Деталь ножниц в Barber Shop Valencia"),
    ("Work area at Barber Shop Valencia", "Рабочая зона Barber Shop Valencia"),
    ("9 October at Barber Shop Valencia", "9 октября в Barber Shop Valencia"),
    ("The barbershop", "Барбершоп"),
    ("The shop", "Салон"),
    ("Tap a photo to view it larger.", "Нажмите на фото, чтобы увеличить."),
    ("Our people", "Наша команда"),
    ("Barber photos will replace the silhouette placeholders.",
     "Фото барберов появятся вместо силуэтов."),
    ("El Carmen menu", "Меню El Carmen"),
    ("La Petxina menu", "Меню La Petxina"),
    ("Each “Book here” opens this shop’s services on Booksy. Next to it, the same service on WhatsApp.",
     "«Записаться» открывает услуги этого салона в Booksy. Рядом — та же услуга в WhatsApp."),
    ("We’re open", "Мы открыты"),
    ("At Juan Llorens", "На Juan Llorens"),
    ("At Juan Llorens 18. Haircuts, beard work and skin treatments in La Petxina.",
     "На Juan Llorens 18. Стрижки, борода и уходы за кожей в районе La Petxina."),
    ("The Carmen shop on Calle Baja. Cuts, fades and beard work with Camilo, Dani and the house standard.",
     "Салон El Carmen на Calle Baja. Стрижки, фейды и борода с Camilo, Dani и стандартом дома."),
    ("Silhouette of", "Силуэт"),
    ("Photo coming soon.", "Скоро будет фото."),
    ("The menu, shop by shop", "Меню по салонам"),
    ("Each service shows its price. “Book here” opens that shop’s Booksy menu. Next to it, the same service on WhatsApp.",
     "У каждой услуги своя цена. «Записаться» открывает меню салона в Booksy. Рядом — WhatsApp."),
    ("Write to us", "Напишите нам"),
    ("Suggestions, questions or compliments. The message is prepared for info@barbershopvalencia.com.",
     "Предложения, вопросы или отзывы. Сообщение готовится для info@barbershopvalencia.com."),
    ("Type of message", "Тип сообщения"),
    ("Tell us your suggestion, question or compliment",
     "Расскажите предложение, вопрос или отзыв"),
    ("Suggestion", "Предложение"),
    ("Question", "Вопрос"),
    ("Compliment", "Отзыв"),
    ("Send", "Отправить"),
    ("<span>Name</span>", "<span>Имя</span>"),
    ("<span>Phone</span>", "<span>Телефон</span>"),
    ("<span>Message</span>", "<span>Сообщение</span>"),
    ("<span>Email</span>", "<span>Email</span>"),
    ("Our shops", "Наши салоны"),
    ("Choose your shop", "Выберите салон"),
    ("Opening hours", "Часы работы"),
    ("Monday to Friday", "Понедельник–пятница"),
    ("Saturday", "Суббота"),
    ("Sunday", "Воскресенье"),
    ("Hours", "Часы"),
    ("Brands we work with", "Бренды, с которыми работаем"),
    ("Brand carousel", "Карусель брендов"),
    ("Social networks", "Соцсети"),
    ("Book by location", "Запись по салону"),
    ("Book El Carmen", "Запись El Carmen"),
    ("Book La Petxina", "Запись La Petxina"),
    ("View the shop", "Смотреть салон"),
    ("Book on WhatsApp", "Запись в WhatsApp"),
    ("Book on Booksy", "Запись в Booksy"),
    ("Book here", "Записаться"),
    ("Book now", "Записаться сейчас"),
    ("See full menu", "Всё меню"),
    ("Open Booksy", "Открыть Booksy"),
    ("Open menu", "Открыть меню"),
    ('aria-label="Language"', 'aria-label="Язык"'),
    (">Services</a>", ">Услуги</a>"),
    (">Contact</a>", ">Контакты</a>"),
    (">Home</a>", ">Главная</a>"),
    (">Book</a>", ">Запись</a>"),
    ("Team", "Команда"),
    (">Barber</p>", ">Барбер</p>"),
    ('"Spain"', '"Испания"'),
    ("Valencian Community", "Валенсийское сообщество"),
    ('"inLanguage": "en-GB"', '"inLanguage": "ru-RU"'),
    ('lang="en"', 'lang="ru"'),
    ('og:locale" content="en_GB"', 'og:locale" content="ru_RU"'),
    ('og:locale" content="es_ES"', 'og:locale" content="ru_RU"'),
    # Service names (common)
    ("Classic cut", "Классическая стрижка"),
    ("Classic cut / fade", "Классическая стрижка / фейд"),
    ("Skin fade", "Skin fade"),
    ("VIP scissor cut", "VIP-стрижка ножницами"),
    ("Beard trim", "Оформление бороды"),
    ("Hot towel shave", "Бритьё с горячим полотенцем"),
    ("Hair wash", "Мытьё головы"),
    ("Kids cut", "Детская стрижка"),
    ("Student cut", "Студенческая стрижка"),
    ("Cut + beard", "Стрижка + борода"),
    ("Facial clay cleanse", "Глиняная чистка лица"),
    ("Machine on the sides and scissors on top.", "Машинка по бокам и ножницы сверху."),
    ("Extreme fade blended into the skin.", "Сильный фейд, сходящий в кожу."),
    ("Full scissor cut with finish.", "Полная стрижка ножницами с финишем."),
]


def lang_switch(lang: str, page: str) -> str:
    """page is filename in that language (es may use servicios/contacto)."""
    es_page = {
        "index.html": "index.html",
        "el-carmen.html": "el-carmen.html",
        "la-petxina.html": "la-petxina.html",
        "services.html": "servicios.html",
        "contact.html": "contacto.html",
        "servicios.html": "servicios.html",
        "contacto.html": "contacto.html",
    }.get(page, page)
    en_page = {
        "servicios.html": "services.html",
        "contacto.html": "contact.html",
    }.get(page, page if page in PAGE_MAP else page)
    ru_page = en_page  # RU uses EN filenames

    def href(target_lang: str, fname: str) -> str:
        if target_lang == lang:
            return f"./{fname}"
        return f"../{target_lang}/{fname}"

    labels = {"es": "Idioma", "en": "Language", "ru": "Язык"}
    return f"""      <div class="lang" aria-label="{labels.get(lang, 'Language')}">
        <a{" class=\"is-active\"" if lang == "es" else ""} href="{href("es", es_page)}" hreflang="es">ES</a>
        <a{" class=\"is-active\"" if lang == "en" else ""} href="{href("en", en_page)}" hreflang="en">EN</a>
        <a{" class=\"is-active\"" if lang == "ru" else ""} href="{href("ru", ru_page)}" hreflang="ru">RU</a>
      </div>
"""


def hreflang_block(page_key: str) -> str:
    """page_key is logical: index, el-carmen, la-petxina, services, contact."""
    es_name = {
        "index": "index.html",
        "el-carmen": "el-carmen.html",
        "la-petxina": "la-petxina.html",
        "services": "servicios.html",
        "contact": "contacto.html",
    }[page_key]
    en_name = {
        "index": "index.html",
        "el-carmen": "el-carmen.html",
        "la-petxina": "la-petxina.html",
        "services": "services.html",
        "contact": "contact.html",
    }[page_key]
    ru_name = en_name

    def url(lang: str, name: str) -> str:
        if name == "index.html":
            return f"{BASE}/{lang}/"
        return f"{BASE}/{lang}/{name}"

    return (
        f'  <link rel="alternate" hreflang="es" href="{url("es", es_name)}">\n'
        f'  <link rel="alternate" hreflang="en" href="{url("en", en_name)}">\n'
        f'  <link rel="alternate" hreflang="ru" href="{url("ru", ru_name)}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{url("es", es_name)}">\n'
    )


def page_key_from_en(name: str) -> str:
    return {
        "index.html": "index",
        "el-carmen.html": "el-carmen",
        "la-petxina.html": "la-petxina",
        "services.html": "services",
        "contact.html": "contact",
    }[name]


def apply_switch_and_hreflang(html: str, lang: str, page_file: str) -> str:
    key = page_key_from_en(
        page_file.replace("servicios.html", "services.html").replace("contacto.html", "contact.html")
    )
    html = re.sub(r'  <link rel="alternate" hreflang="[^"]+" href="[^"]*">\n', "", html)
    html = html.replace('<link rel="canonical"', hreflang_block(key) + "  <link rel=\"canonical\"", 1)
    html = re.sub(r'      <div class="lang"[\s\S]*?</div>\n', "", html)
    switch = lang_switch(lang, page_file)
    for marker in (
        '<a class="btn btn--ghost" href="#reservar">',
        '<a class="btn btn--ghost" href="https://booksy.com',
        '<a class="btn btn--primary" href="https://api.whatsapp.com',
    ):
        if marker in html:
            html = html.replace(marker, switch + "      " + marker, 1)
            break
    return html


def translate_en_to_ru(html: str) -> str:
    for src, dst in RU_FROM_EN:
        html = html.replace(src, dst)
    # WhatsApp EN → RU ("Здравствуйте, хочу записаться" / " в Barber Shop Valencia")
    html = html.replace(
        "Hi%2C%20I%20want%20to%20book",
        "%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5%2C%20%D1%85%D0%BE%D1%87%D1%83%20%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D0%B0%D1%82%D1%8C%D1%81%D1%8F",
    )
    html = html.replace("%20at%20Barber%20Shop%20Valencia", "%20%D0%B2%20Barber%20Shop%20Valencia")
    # Keywords Russian-focused
    html = re.sub(
        r'<meta name="keywords" content="[^"]*">',
        '<meta name="keywords" content="барбершоп валенсия, barber shop valencia, барбершоп в валенсии, стрижка валенсия, борода валенсия, барбер рядом, El Carmen, La Petxina, barbershoop">',
        html,
        count=1,
    )
    # Fix broken leftovers
    html = html.replace("Book por local", "Запись по салону")
    html = html.replace("Запись by location", "Запись по салону")
    html = html.replace("España", "Испания")
    # Breadcrumbs (schema name fields only)
    html = html.replace('"name": "Home"', '"name": "Главная"')
    html = html.replace('"name": "Services"', '"name": "Услуги"')
    html = html.replace('"name": "Contact"', '"name": "Контакты"')
    # SEO base paths en→ru (avoid double-replacing already /ru/)
    html = html.replace(f"{BASE}/en/", f"{BASE}/ru/")
    # Blog teaser slugs
    html = html.replace(
        "./blog/9-october-valencia-barbershop-open-la-petxina.html",
        "./blog/9-oktyabrya-valensiya-barbershop-open-la-petxina.html",
    )
    html = html.replace("./blog/barbershop-in-valencia.html", "./blog/barbershop-v-valensii.html")
    html = html.replace("./blog/appointment-barbershop-valencia.html", "./blog/zapis-v-barbershop-valensiya.html")
    html = html.replace(">Blog</a>", ">Блог</a>")
    html = html.replace("See all blog posts", "Смотреть весь блог")
    return html


def patch_existing_lang(lang_dir: str, page_files: list[str]) -> None:
    d = ROOT / lang_dir
    for name in page_files:
        path = d / name
        if not path.exists():
            continue
        html = path.read_text()
        html = apply_switch_and_hreflang(html, lang_dir, name)
        path.write_text(html)
        print(f"patched {lang_dir}/{name}")


RU_META = {
    "index.html": {
        "title": "Barber Shop Valencia | Барбершоп в Валенсии · El Carmen и La Petxina",
        "description": "Барбершоп в Валенсии для мужчин. Два салона: El Carmen (C/ Baja 50) и La Petxina (C/ Juan Llorens 18). Стрижки, борода и запись онлайн.",
        "og_title": "Barber Shop Valencia | Барбершоп в Валенсии",
        "og_description": "Барбершоп Валенсия в El Carmen и La Petxina. Запишитесь на стрижку или бороду.",
    },
    "el-carmen.html": {
        "title": "Barber Shop Valencia El Carmen | Барбершоп на C/ Baja 50",
        "description": "Barber Shop Valencia El Carmen — барбершоп в Валенсии на C/ Baja 50. Мужские стрижки, фейды и борода. Запись в Booksy или WhatsApp.",
        "og_title": "Barber Shop Valencia El Carmen",
        "og_description": "Барбершоп El Carmen на C/ Baja 50. Запись на стрижку или бороду.",
    },
    "la-petxina.html": {
        "title": "Барбершоп La Petxina Валенсия | Barber Shop Valencia",
        "description": "Barber Shop Valencia в La Petxina — барбершоп на C/ Juan Llorens 18. Стрижки, борода и уходы. Запись в Booksy или WhatsApp.",
        "og_title": "Барбершоп La Petxina | Barber Shop Valencia",
        "og_description": "Барбершоп в Валенсии · La Petxina, C/ Juan Llorens 18.",
    },
    "services.html": {
        "title": "Услуги и цены | Барбершоп Валенсия · Barber Shop Valencia",
        "description": "Меню барбершопа в Валенсии: стрижки, борода и уходы в El Carmen и La Petxina. Цены и запись онлайн.",
        "og_title": "Услуги и цены | Barber Shop Valencia",
        "og_description": "Услуги барбершопа в El Carmen и La Petxina. Запись по салону.",
    },
    "contact.html": {
        "title": "Контакты | Barber Shop Valencia · Барберы рядом",
        "description": "Свяжитесь с Barber Shop Valencia: WhatsApp +34 677 142 958. Барбершоп в Валенсии — El Carmen и La Petxina.",
        "og_title": "Контакты | Barber Shop Valencia",
        "og_description": "Барберы рядом в Валенсии. El Carmen и La Petxina.",
    },
}


def set_meta(html: str, meta: dict) -> str:
    html = re.sub(r"<title>[^<]*</title>", f"<title>{meta['title']}</title>", html, count=1)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{meta["description"]}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{meta["og_title"]}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{meta["og_description"]}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{meta["og_title"]}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta name="twitter:description" content="[^"]*">',
        f'<meta name="twitter:description" content="{meta["og_description"]}">',
        html,
        count=1,
    )
    return html


def build_ru_pages() -> None:
    en_dir = ROOT / "en"
    ru_dir = ROOT / "ru"
    ru_dir.mkdir(exist_ok=True)

    for en_name in PAGE_MAP:
        src = (en_dir / en_name).read_text()
        html = translate_en_to_ru(src)
        html = set_meta(html, RU_META[en_name])
        html = apply_switch_and_hreflang(html, "ru", en_name)
        if 'href="./blog/"' not in html and 'href="./services.html"' in html:
            html = html.replace(
                '<a href="./services.html">Услуги</a>',
                '<a href="./services.html">Услуги</a>\n      <a href="./blog/">Блог</a>',
                1,
            )
        else:
            html = html.replace(">Blog</a>", ">Блог</a>")
        if en_name == "index.html":
            html = re.sub(
                r'<link rel="canonical" href="[^"]*">',
                f'<link rel="canonical" href="{BASE}/ru/">',
                html,
                count=1,
            )
            html = re.sub(
                r'<meta property="og:url" content="[^"]*">',
                f'<meta property="og:url" content="{BASE}/ru/">',
                html,
                count=1,
            )
        else:
            html = re.sub(
                r'<link rel="canonical" href="[^"]*">',
                f'<link rel="canonical" href="{BASE}/ru/{en_name}">',
                html,
                count=1,
            )
            html = re.sub(
                r'<meta property="og:url" content="[^"]*">',
                f'<meta property="og:url" content="{BASE}/ru/{en_name}">',
                html,
                count=1,
            )
        # Hero fallbacks if still Spanish/English mix
        html = html.replace("Cortes precisos. Estilo actual.", "Точные стрижки. Актуальный стиль.")
        html = html.replace(
            "Dos tiendas en Valencia. Un corte limpio, una barba definida y un equipo que cuida el detalle.",
            "Два салона в Валенсии. Чистая стрижка, чёткая борода и команда, которая ценит детали.",
        )
        html = html.replace("Reservar por local", "Запись по салону")
        html = html.replace("Book por local", "Запись по салону")
        html = html.replace("Precise cuts. Current style.", "Точные стрижки. Актуальный стиль.")
        (ru_dir / en_name).write_text(html)
        print(f"ok ru/{en_name}")


def update_root_and_sitemap() -> None:
    (ROOT / "index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Barber Shop Valencia</title>
  <meta name="robots" content="noindex, follow">
  <link rel="alternate" hreflang="es" href="{BASE}/es/">
  <link rel="alternate" hreflang="en" href="{BASE}/en/">
  <link rel="alternate" hreflang="ru" href="{BASE}/ru/">
  <link rel="alternate" hreflang="x-default" href="{BASE}/es/">
  <link rel="canonical" href="{BASE}/es/">
  <meta http-equiv="refresh" content="0; url=es/">
  <script>
    location.replace("es/");
  </script>
</head>
<body>
  <p><a href="es/">Español</a> · <a href="en/">English</a> · <a href="ru/">Русский</a></p>
</body>
</html>
"""
    )

    from datetime import date

    today = date.today().isoformat()
    urls = []
    maps = {
        "es": ["index.html", "el-carmen.html", "la-petxina.html", "servicios.html", "contacto.html"],
        "en": ["index.html", "el-carmen.html", "la-petxina.html", "services.html", "contact.html"],
        "ru": ["index.html", "el-carmen.html", "la-petxina.html", "services.html", "contact.html"],
    }
    for lang, pages in maps.items():
        for page in pages:
            loc = f"{BASE}/{lang}/" if page == "index.html" else f"{BASE}/{lang}/{page}"
            priority = "1.0" if page == "index.html" else "0.9"
            urls.append(
                f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>"""
            )

    blog = {
        "es": [
            "index.html",
            "9-octubre-valencia-barberia-abierta-la-petxina.html",
            "barberia-en-valencia.html",
            "barberia-cita-previa-valencia.html",
            "corte-pelo-hombre-valencia.html",
            "mejor-barberia-valencia.html",
        ],
        "en": [
            "index.html",
            "9-october-valencia-barbershop-open-la-petxina.html",
            "barbershop-in-valencia.html",
            "appointment-barbershop-valencia.html",
            "mens-haircut-valencia.html",
            "best-barbershop-valencia.html",
        ],
        "ru": [
            "index.html",
            "9-oktyabrya-valensiya-barbershop-open-la-petxina.html",
            "barbershop-v-valensii.html",
            "zapis-v-barbershop-valensiya.html",
            "muzhskaya-strizhka-valensiya.html",
            "luchshiy-barbershop-valensiya.html",
        ],
    }
    for lang, pages in blog.items():
        for page in pages:
            # only add if file exists (blog ru may be generated after)
            path = ROOT / lang / "blog" / page
            if page != "index.html" and not path.exists() and lang == "ru":
                continue
            if lang != "ru" or path.exists() or page == "index.html":
                if lang == "ru" and page != "index.html" and not path.exists():
                    continue
            loc = f"{BASE}/{lang}/blog/" if page == "index.html" else f"{BASE}/{lang}/blog/{page}"
            if lang == "ru" and page != "index.html" and not (ROOT / lang / "blog" / page).exists():
                continue
            urls.append(
                f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"0.85" if page == "index.html" else "0.8"}</priority>
  </url>"""
            )

    # Deduplicate locs
    seen = set()
    unique = []
    for u in urls:
        m = re.search(r"<loc>([^<]+)</loc>", u)
        loc = m.group(1) if m else u
        if loc in seen:
            continue
        seen.add(loc)
        unique.append(u)

    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(unique)
        + "\n</urlset>\n"
    )


def main() -> None:
    build_ru_pages()
    patch_existing_lang("es", ["index.html", "el-carmen.html", "la-petxina.html", "servicios.html", "contacto.html"])
    patch_existing_lang("en", ["index.html", "el-carmen.html", "la-petxina.html", "services.html", "contact.html"])
    update_root_and_sitemap()
    print("done")


if __name__ == "__main__":
    main()
