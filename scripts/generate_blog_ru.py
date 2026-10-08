#!/usr/bin/env python3
"""Generate Russian blog (/ru/blog) and patch ES/EN blog lang switchers with RU."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://barbershopvalencia.es"

from analytics import ensure_gtag  # noqa: E402
BOOKSY_PETXINA = "https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia"
WA = "https://api.whatsapp.com/send/?phone=34677142958&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5%2C%20%D1%85%D0%BE%D1%87%D1%83%20%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D0%B0%D1%82%D1%8C%D1%81%D1%8F%20%D0%B2%20Barber%20Shop%20Valencia%20La%20Petxina.&type=phone_number&app_absent=0"

FOOTER = """<footer class="footer">
    <div class="container footer__grid">
      <div>
        <h3>Barber Shop Valencia</h3>
        <p>Два барбершопа в Валенсии. Стрижки, борода и мужской уход с командой, которая следит за деталями.</p>
        <div class="socials" aria-label="Соцсети">
        <a href="https://www.instagram.com/barbershopvalencia_/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm5 4.2A4.8 4.8 0 1 0 16.8 12 4.8 4.8 0 0 0 12 7.2zm6.3-.8a1.15 1.15 0 1 0 1.15 1.15A1.15 1.15 0 0 0 18.3 6.4zM12 9.1A2.9 2.9 0 1 1 9.1 12 2.9 2.9 0 0 1 12 9.1z"/></svg></a>
        <a href="https://www.tiktok.com/search?q=Barber%20Shop%20Valencia" target="_blank" rel="noopener" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.2 3h2.3a5.2 5.2 0 0 0 3.4 3.2v2.3a7.4 7.4 0 0 1-3.4-1.1v7.1a6 6 0 1 1-6-6c.3 0 .7 0 1 .1v2.5a3.5 3.5 0 1 0 2.5 3.4V3z"/></svg></a>
        <a href="https://www.facebook.com/barbershop.valencia.9" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.2 8.5H17V5.4h-2.8c-2.3 0-4.1 1.8-4.1 4.1v2H8v3.1h2.1V21h3.2v-6.4h2.7l.4-3.1h-3.1v-1.6c0-.7.4-1.4 1.4-1.4z"/></svg></a>
        <a href="https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia" target="_blank" rel="noopener" aria-label="Booksy"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2.8h2.1V5h5.8V2.8H17V5h1.6A2.4 2.4 0 0 1 21 7.4V19a2.4 2.4 0 0 1-2.4 2.4H5.4A2.4 2.4 0 0 1 3 19V7.4A2.4 2.4 0 0 1 5.4 5H7zm12 7.2H5v9h14z"/></svg></a>
      </div>
      </div>
      <div>
        <h3>La Petxina</h3>
        <address>
          <p><a href="https://www.google.com/maps/search/?api=1&query=C%2F+Juan+Llorens+18%2C+46008+Valencia" target="_blank" rel="noopener">C/ Juan Llorens 18<br>46008 Valencia, Испания</a></p>
        </address>
      </div>
      <div>
        <h3>El Carmen</h3>
        <address>
          <p><a href="https://www.google.com/maps/search/?api=1&query=C%2F+Baja+50%2C+46008+Valencia" target="_blank" rel="noopener">C/ Baja, 50<br>46008 Valencia, Испания</a></p>
        </address>
      </div>
    </div>
    <div class="container footer__base">
      <p>© Barber Shop Valencia</p>
      <p><a href="mailto:info@barbershopvalencia.com">info@barbershopvalencia.com</a></p>
    </div>
  </footer>
  <a class="wa" href="https://api.whatsapp.com/send/?phone=34677142958&text&type=phone_number&app_absent=0" target="_blank" rel="noopener" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 3.2A8.7 8.7 0 0 0 4.5 16.3L3.4 20.6l4.4-1.1a8.7 8.7 0 0 0 4.2 1.1h.1A8.7 8.7 0 0 0 12.04 3.2zm5 12.2c-.2.6-1.2 1.1-1.6 1.1-.4.1-.9.1-2.9-.6-2.4-1-4-3.4-4.1-3.6-.1-.2-1-1.3-1-2.5s.6-1.8.9-2 .5-.3.7-.3h.6c.2 0 .4 0 .6.5.2.6.7 1.9.8 2s0 .4-.1.5-.3.4-.4.6-.3.3-.1.7a7.4 7.4 0 0 0 1.4 1.7 6.4 6.4 0 0 0 2 1.1c.3.1.5 0 .7-.2s.8-.9 1-1.2.4-.3.6-.2 1.6.8 1.9 1 .4.4.3.7z"/></svg>
  </a>
  <script src="../../assets/site.js"></script>
</body>
</html>
"""

POSTS = [
    {
        "slug": "9-oktyabrya-valensiya-barbershop-open-la-petxina.html",
        "es": "9-octubre-valencia-barberia-abierta-la-petxina.html",
        "en": "9-october-valencia-barbershop-open-la-petxina.html",
        "date": "2026-10-08",
        "date_label": "8 октября 2026",
        "image": "IMG_0842.jpg",
        "image_alt": "Barber Shop Valencia к 9 октября",
        "title": "9 октября в Валенсии: что означает и барбершоп открыт в La Petxina",
        "desc": "9 октября — День Валенсийского сообщества. Чем заняться, стрижки к празднику и запись в La Petxina (открыта). El Carmen закрыт.",
        "excerpt": "Праздник 9 d’octubre: La Petxina открыта, El Carmen закрыт. Идеи на день и образы для праздника.",
        "body": f"""
        <p class="blog-notice"><strong>Особый график 9 октября:</strong> <a href="../la-petxina.html">La Petxina</a> (C/ Juan Llorens 18) <strong>открыта</strong>. <a href="../el-carmen.html">El Carmen</a> (C/ Baja 50) <strong>закрыт</strong>.</p>
        <p><strong>9 октября</strong> — <strong>День Валенсийского сообщества</strong> (Nou d’Octubre). Дата отмечает вход короля Жауме I в Валенсию в 1238 году — символ валенсийской идентичности и официальный праздник во всей Comunitat.</p>
        <h2>Что означает 9 октября в Валенсии</h2>
        <p>Это не только выходной: гражданская процессия с Reial Senyera, подношение Жауме I, гимн, масклета и днём парад Моров и христиан. Также отмечают Sant Donís с традицией дарить марципановую <em>mocadorà</em>.</p>
        <h2>Чем заняться в Валенсии 9 октября</h2>
        <ul>
          <li><strong>Утро в центре:</strong> процессия от площади Ajuntament к собору и статуе Жауме I.</li>
          <li><strong>Масклета:</strong> обычно на площади Ajuntament после процессии.</li>
          <li><strong>День:</strong> парад Моров и христиан по центру.</li>
          <li><strong>Sant Donís:</strong> mocadorà — сладкий символ дня.</li>
          <li><strong>Прогулка:</strong> vermut или обед рядом с El Carmen, Ruzafa или La Petxina.</li>
        </ul>
        <h2>Стрижки к празднику</h2>
        <ul>
          <li><strong>Чистый fade + борода:</strong> самый популярный образ.</li>
          <li><strong>Текстурный crop:</strong> современно и удобно на весь день.</li>
          <li><strong>Классика с переходом:</strong> для семейных и официальных моментов.</li>
          <li><strong>Стрижка + борода:</strong> быстрый апгрейд к празднику.</li>
        </ul>
        <h2>Запись в La Petxina (открыта 9 октября)</h2>
        <p>В этот день <strong>работает только La Petxina</strong>, C/ Juan Llorens 18. El Carmen закрыт.</p>
        <p>
          <a class="btn btn--primary" href="{BOOKSY_PETXINA}" target="_blank" rel="noopener">Запись · La Petxina (Booksy)</a>
          <a class="btn btn--ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp</a>
        </p>
        """,
    },
    {
        "slug": "barbershop-v-valensii.html",
        "es": "barberia-en-valencia.html",
        "en": "barbershop-in-valencia.html",
        "date": "2026-10-06",
        "date_label": "6 октября 2026",
        "image": "IMG_0860.jpg",
        "image_alt": "Интерьер Barber Shop Valencia",
        "title": "Барбершоп в Валенсии: мужской стиль и профессиональный сервис",
        "desc": "Ищете барбершоп в Валенсии с современными стрижками и лёгкой записью? Barber Shop Valencia в El Carmen и La Petxina.",
        "excerpt": "Два салона в Валенсии, опытные барберы и онлайн-запись.",
        "body": """
        <p>Если вам нужен <strong>барбершоп в Валенсии</strong> с качеством и вниманием к деталям — Barber Shop Valencia. Два адреса: El Carmen (C/ Baja 50) и La Petxina (C/ Juan Llorens 18).</p>
        <h2>Почему выбирают нас</h2>
        <ul>
          <li>Центральные локации: El Carmen и La Petxina.</li>
          <li>Барберы с акцентом на чистый финиш.</li>
          <li>Запись в Booksy или WhatsApp.</li>
          <li>Одинаковый график в обоих салонах.</li>
        </ul>
        <h2>Где нас найти</h2>
        <p><a href="../el-carmen.html">El Carmen</a> — C/ Baja 50.<br>
        <a href="../la-petxina.html">La Petxina</a> — C/ Juan Llorens 18.</p>
        <p>Смотрите <a href="../services.html">меню услуг</a> и записывайтесь.</p>
        """,
    },
    {
        "slug": "zapis-v-barbershop-valensiya.html",
        "es": "barberia-cita-previa-valencia.html",
        "en": "appointment-barbershop-valencia.html",
        "date": "2026-10-03",
        "date_label": "3 октября 2026",
        "image": "IMG_0834.jpg",
        "image_alt": "Кресло в Barber Shop Valencia",
        "title": "Барбершоп с записью в Валенсии: ваш стиль без ожидания",
        "desc": "Запишитесь в барбершоп Валенсии заранее. Стрижки и борода в El Carmen или La Petxina через Booksy или WhatsApp.",
        "excerpt": "Онлайн-запись, приходите ко времени — без лишней очереди.",
        "body": """
        <p>В Barber Shop Valencia ваше время важно. Поэтому мы работаем <strong>по записи</strong>: приходите к своему слоту и садитесь в кресло без длинной очереди.</p>
        <h2>Как записаться за 3 шага</h2>
        <ol>
          <li>Выберите салон: <a href="../el-carmen.html">El Carmen</a> или <a href="../la-petxina.html">La Petxina</a>.</li>
          <li>Выберите услугу в <a href="../services.html">меню</a>.</li>
          <li>Подтвердите время в Booksy или напишите в WhatsApp.</li>
        </ol>
        """,
    },
    {
        "slug": "muzhskaya-strizhka-valensiya.html",
        "es": "corte-pelo-hombre-valencia.html",
        "en": "mens-haircut-valencia.html",
        "date": "2026-09-28",
        "date_label": "28 сентября 2026",
        "image": "IMG_0858.jpg",
        "image_alt": "Салон готов к стрижке",
        "title": "Мужская стрижка в Валенсии: практичный гид 2026",
        "desc": "Мужская стрижка в Валенсии: fade, crop, классика и борода. Запись в El Carmen или La Petxina.",
        "excerpt": "Что попросить в кресле, сколько длится стрижка и как поддерживать форму.",
        "body": """
        <p>Ищете <strong>мужскую стрижку в Валенсии</strong>? В Barber Shop Valencia делаем актуальные и классические техники в El Carmen и La Petxina.</p>
        <h2>Популярные стили 2026</h2>
        <ul>
          <li><strong>Fade / skin fade</strong> — чисто и универсально.</li>
          <li><strong>Textured crop</strong> — современно, с движением.</li>
          <li><strong>Undercut</strong> — короткие бока и объём сверху.</li>
          <li><strong>Классика с переходом</strong> — для работы и выходных.</li>
        </ul>
        <p>Обычно стрижка занимает около 30 минут. Рекомендуем обновлять каждые 3–4 недели.</p>
        """,
    },
    {
        "slug": "luchshiy-barbershop-valensiya.html",
        "es": "mejor-barberia-valencia.html",
        "en": "best-barbershop-valencia.html",
        "date": "2026-09-22",
        "date_label": "22 сентября 2026",
        "image": "IMG_0820.jpg",
        "image_alt": "Атмосфера барбершопа в Валенсии",
        "title": "Лучший барбершоп в Валенсии: почему выбирают Barber Shop Valencia",
        "desc": "Почему ищут лучший барбершоп в Валенсии у Barber Shop Valencia: стрижки, борода, атмосфера и два центральных адреса.",
        "excerpt": "Качество стрижки, комфорт и два удобных адреса в Валенсии.",
        "body": """
        <p>Когда ищут <strong>лучший барбершоп в Валенсии</strong>, смотрят не только на цену — на финиш, сервис и атмосферу. В Barber Shop Valencia соединяем мастерство и внимание к деталям.</p>
        <h2>Что нас отличает</h2>
        <ul>
          <li>Современные и классические стрижки.</li>
          <li>Полный уход за бородой.</li>
          <li>Традиционное бритьё.</li>
          <li>Уходы для кожи и волос.</li>
          <li>Советы по стилю под вашу форму лица.</li>
        </ul>
        <p>Запись: <a href="../el-carmen.html">El Carmen</a> или <a href="../la-petxina.html">La Petxina</a>.</p>
        """,
    },
]


def nav(slug: str | None = None) -> str:
    if slug is None:
        es_href = "../../es/blog/index.html"
        en_href = "../../en/blog/index.html"
        ru_href = "./index.html"
    else:
        p = next(x for x in POSTS if x["slug"] == slug)
        es_href = f"../../es/blog/{p['es']}"
        en_href = f"../../en/blog/{p['en']}"
        ru_href = f"./{slug}"
    return f"""<header class="nav">
    <a class="nav__brand" href="../index.html"><img src="../../assets/logo-bw-transparent.png" alt="Barber Shop Valencia" width="56" height="62">Barber Shop Valencia</a>
    <button class="nav__toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="Открыть меню"><span></span></button>
    <nav class="nav__links" data-nav>
      <a href="../index.html">Главная</a>
      <div class="nav__drop">
        <a href="../index.html#tiendas" data-drop-toggle aria-expanded="false">Наши салоны</a>
        <ul class="dropdown">
          <li><a href="../el-carmen.html">El Carmen</a></li>
          <li><a href="../la-petxina.html">La Petxina</a></li>
        </ul>
      </div>
      <a href="../services.html">Услуги</a>
      <a href="./index.html" class="is-active">Блог</a>
      <a href="../contact.html">Контакты</a>
      <div class="lang" aria-label="Язык">
        <a href="{es_href}" hreflang="es">ES</a>
        <a href="{en_href}" hreflang="en">EN</a>
        <a class="is-active" href="{ru_href}" hreflang="ru">RU</a>
      </div>
      <a class="btn btn--ghost" href="{BOOKSY_PETXINA}" target="_blank" rel="noopener">Booksy</a>
      <a class="btn btn--primary" href="https://api.whatsapp.com/send/?phone=34677142958&text&type=phone_number&app_absent=0" target="_blank" rel="noopener">WhatsApp</a>
    </nav>
  </header>
"""


def head(title: str, desc: str, canonical: str, es_h: str, en_h: str, ru_h: str, og_image: str, article: bool = False) -> str:
    schema = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "{"BlogPosting" if article else "Blog"}",
    "headline": "{title}",
    "description": "{desc}",
    "image": "{og_image}",
    "url": "{canonical}",
    "inLanguage": "ru-RU",
    "publisher": {{ "@type": "Organization", "name": "Barber Shop Valencia" }}
  }}
  </script>"""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Barber Shop Valencia</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="барбершоп валенсия, barber shop valencia, барбершоп в валенсии, стрижка валенсия, barbershoop">
  <meta name="robots" content="index, follow">
  <link rel="alternate" hreflang="es" href="{es_h}">
  <link rel="alternate" hreflang="en" href="{en_h}">
  <link rel="alternate" hreflang="ru" href="{ru_h}">
  <link rel="alternate" hreflang="x-default" href="{es_h}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="{"article" if article else "website"}">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:site_name" content="Barber Shop Valencia">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_image}">
  <meta name="theme-color" content="#121210">
  <link rel="icon" href="../../assets/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="../../assets/favicon-32.png">
  <link rel="apple-touch-icon" href="../../assets/apple-touch-icon.png">
  <link rel="manifest" href="../../site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=Rye&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/style.css">{schema}
</head>
<body>
"""


def write_index() -> None:
    out = ROOT / "ru" / "blog"
    out.mkdir(parents=True, exist_ok=True)
    title = "Блог барбершопа в Валенсии"
    desc = "Советы по стрижкам, бороде и стилю в Валенсии. Статьи Barber Shop Valencia."
    html = head(
        title, desc, f"{BASE}/ru/blog/",
        f"{BASE}/es/blog/", f"{BASE}/en/blog/", f"{BASE}/ru/blog/",
        f"{BASE}/assets/el-carmen/web/IMG_0860.jpg",
    )
    html += nav()
    html += f"""
  <section class="section blog-hero">
    <div class="container">
      <p class="section__label">Блог</p>
      <h1 class="section__title">{title}</h1>
      <p class="section__lead">Тренды, советы и новости Barber Shop Valencia в El Carmen и La Petxina.</p>
    </div>
  </section>
  <section class="section section--alt">
    <div class="container blog-grid">
"""
    for p in POSTS:
        html += f"""
      <article class="blog-card">
        <a class="blog-card__media" href="./{p['slug']}">
          <img src="../../assets/el-carmen/web/{p['image']}" alt="{p['image_alt']}" width="1200" height="900" loading="lazy">
        </a>
        <div class="blog-card__body">
          <time datetime="{p['date']}">{p['date_label']}</time>
          <h2><a href="./{p['slug']}">{p['title']}</a></h2>
          <p>{p['excerpt']}</p>
          <a class="btn btn--ghost btn--sm" href="./{p['slug']}">Читать</a>
        </div>
      </article>
"""
    html += "</div></section>\n" + FOOTER
    (out / "index.html").write_text(ensure_gtag(html))
    print("ok ru/blog/index.html")


def write_posts() -> None:
    for p in POSTS:
        can = f"{BASE}/ru/blog/{p['slug']}"
        html = head(
            p["title"], p["desc"], can,
            f"{BASE}/es/blog/{p['es']}", f"{BASE}/en/blog/{p['en']}", can,
            f"{BASE}/assets/el-carmen/web/{p['image']}",
            article=True,
        )
        html += nav(p["slug"])
        html += f"""
  <article class="section blog-post">
    <div class="container blog-post__wrap">
      <p class="blog-post__back"><a href="./index.html">← Назад в блог</a></p>
      <header class="blog-post__header">
        <p class="section__label">Блог</p>
        <h1 class="section__title">{p['title']}</h1>
        <time datetime="{p['date']}">{p['date_label']}</time>
      </header>
      <figure class="blog-post__hero">
        <img src="../../assets/el-carmen/web/{p['image']}" alt="{p['image_alt']}" width="1600" height="1200">
      </figure>
      <div class="blog-post__content prose">
        {p['body']}
      </div>
      <div class="blog-post__cta">
        <h2>Запишитесь</h2>
        <p>Выберите El Carmen или La Petxina и запишитесь через Booksy или WhatsApp.</p>
        <div class="cta__actions cta__actions--stack">
          <a class="btn btn--primary" href="https://booksy.com/es-es/132769_barber-shop-valencia-el-carmen_barberia_58087_valencia" target="_blank" rel="noopener">Запись El Carmen</a>
          <a class="btn btn--ghost" href="{BOOKSY_PETXINA}" target="_blank" rel="noopener">Запись La Petxina</a>
          <a class="btn btn--ghost" href="https://api.whatsapp.com/send/?phone=34677142958&text&type=phone_number&app_absent=0" target="_blank" rel="noopener">WhatsApp</a>
        </div>
      </div>
    </div>
  </article>
"""
        html += FOOTER
        (ROOT / "ru" / "blog" / p["slug"]).write_text(ensure_gtag(html))
        print("ok ru/blog/" + p["slug"])


def patch_other_blogs() -> None:
    """Add RU link to ES/EN blog lang switchers and hreflang."""
    mapping = {p["es"]: (p["en"], p["slug"]) for p in POSTS}
    mapping["index.html"] = ("index.html", "index.html")

    for lang, key in (("es", "es"), ("en", "en")):
        blog = ROOT / lang / "blog"
        for path in blog.glob("*.html"):
            html = path.read_text()
            name = path.name
            if lang == "es":
                ru_name = mapping.get(name, (None, None))[1]
            else:
                # en filename → ru
                ru_name = next((p["slug"] for p in POSTS if p["en"] == name), None)
                if name == "index.html":
                    ru_name = "index.html"
            if not ru_name:
                continue
            ru_href = f"../../ru/blog/{ru_name}"
            # hreflang
            if 'hreflang="ru"' not in html:
                html = html.replace(
                    '<link rel="alternate" hreflang="x-default"',
                    f'<link rel="alternate" hreflang="ru" href="{BASE}/ru/blog/{ru_name}">\n  <link rel="alternate" hreflang="x-default"',
                    1,
                )
            # lang switch: add RU after EN if missing
            if 'hreflang="ru">RU</a>' not in html:
                html = re.sub(
                    r'(<a[^>]*hreflang="en"[^>]*>EN</a>)',
                    rf'\1\n        <a href="{ru_href}" hreflang="ru">RU</a>',
                    html,
                    count=1,
                )
            path.write_text(html)
            print("patched", path.relative_to(ROOT))


def patch_home_teaser() -> None:
    """Add RU blog teaser links on ru/index if blog section exists after build."""
    path = ROOT / "ru" / "index.html"
    if not path.exists():
        return
    html = path.read_text()
    # Translate remaining blog teaser if still English
    reps = [
        ("./blog/9-october-valencia-barbershop-open-la-petxina.html",
         "./blog/9-oktyabrya-valensiya-barbershop-open-la-petxina.html"),
        ("./blog/barbershop-in-valencia.html", "./blog/barbershop-v-valensii.html"),
        ("See all blog posts", "Смотреть весь блог"),
        ("Style and barbershop tips in Valencia", "Стиль и советы барбершопа в Валенсии"),
        ("Haircut, beard and booking tips. The latest articles from Barber Shop Valencia.",
         "Советы по стрижкам, бороде и записи. Последние статьи Barber Shop Valencia."),
    ]
    for a, b in reps:
        html = html.replace(a, b)
    path.write_text(html)


def main() -> None:
    write_index()
    write_posts()
    patch_other_blogs()
    patch_home_teaser()
    print("done")


if __name__ == "__main__":
    main()
