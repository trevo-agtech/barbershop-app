#!/usr/bin/env python3
"""Build /es and /en versions of the Barber Shop Valencia site."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://barbershopvalencia.es"

PAGE_MAP_ES_TO_EN = {
    "index.html": "index.html",
    "el-carmen.html": "el-carmen.html",
    "la-petxina.html": "la-petxina.html",
    "servicios.html": "services.html",
    "contacto.html": "contact.html",
}

# UI / content replacements for EN (order matters: longer phrases first)
EN_REPLACEMENTS: list[tuple[str, str]] = [
    # Nav / chrome
    ("Inicio", "Home"),
    ("Nuestras tiendas", "Our shops"),
    ("Servicios", "Services"),
    ("Contacto", "Contact"),
    ("Reservar", "Book"),
    ("Abrir menú", "Open menu"),
    ("Idioma", "Language"),
    # Common CTAs
    ("Reservar por local", "Book by location"),
    ("Sobre la barbería", "About the barbershop"),
    ("Reservar El Carmen", "Book El Carmen"),
    ("Reservar La Petxina", "Book La Petxina"),
    ("Ver la tienda", "View the shop"),
    ("Reservar por WhatsApp", "Book on WhatsApp"),
    ("Reservar por Booksy", "Book on Booksy"),
    ("Reserva aquí", "Book here"),
    ("Reserva ahora", "Book now"),
    ("Ver toda la carta", "See full menu"),
    ("Abrir Booksy", "Open Booksy"),
    # Sections
    ("Elige tu local", "Choose your shop"),
    ("Cada barbería tiene su carta. Reserva directamente en el local que prefieras.",
     "Each shop has its own menu. Book directly at the location you prefer."),
    ("Cuándo estamos", "Opening hours"),
    ("Mismo horario en El Carmen y en La Petxina. Los festivos pueden variar.",
     "Same hours at El Carmen and La Petxina. Public holidays may vary."),
    ("Lunes a viernes", "Monday to Friday"),
    ("Sábado", "Saturday"),
    ("Domingo", "Sunday"),
    ("Horario", "Hours"),
    ("Marcas con las que trabajamos", "Brands we work with"),
    ("Productos de barbería que usamos en la silla: pomadas, navajas, máquinas y cuidado de piel.",
     "Barber products we use in the chair: pomades, razors, clippers and skincare."),
    ("Partners", "Partners"),
    ("Elige la tienda. Cada una tiene su carta y su enlace de reserva.",
     "Choose a shop. Each one has its own menu and booking link."),
    ("Dos barberías en Valencia. Cortes, barba y cuidado masculino con un equipo que cuida el detalle.",
     "Two barbershops in Valencia. Haircuts, beard work and men’s grooming with a team that minds the details."),
    ("Cortes precisos. Estilo actual.", "Precise cuts. Current style."),
    ("Dos tiendas en Valencia. Un corte limpio, una barba definida y un equipo que cuida el detalle.",
     "Two shops in Valencia. A clean cut, a defined beard and a team that minds the details."),
    ("Interior de Barber Shop Valencia El Carmen", "Interior of Barber Shop Valencia El Carmen"),
    ("Interior de Barber Shop Valencia", "Interior of Barber Shop Valencia"),
    ("Fachada Barber Shop Valencia El Carmen", "Storefront of Barber Shop Valencia El Carmen"),
    ("Corte en Barber Shop Valencia", "Haircut at Barber Shop Valencia"),
    ("Detalle de tijera en Barber Shop Valencia", "Scissor detail at Barber Shop Valencia"),
    ("Escudo Barber Shop Valencia", "Barber Shop Valencia crest"),
    # Shop pages
    ("La barbería", "The barbershop"),
    ("El local", "The shop"),
    ("Pulsa una foto para verla en grande.", "Tap a photo to view it larger."),
    ("Equipo", "Team"),
    ("Nuestra gente", "Our people"),
    ("Las fotos de los barberos entran en el lugar de la silueta.",
     "Barber photos will replace the silhouette placeholders."),
    ("Barbero", "Barber"),
    ("Carta de El Carmen", "El Carmen menu"),
    ("Carta de La Petxina", "La Petxina menu"),
    ("Cada «Reserva aquí» abre los servicios de esta tienda en Booksy. Al lado, el mismo servicio por WhatsApp.",
     "Each “Book here” opens this shop’s services on Booksy. Next to it, the same service on WhatsApp."),
    ("Abrimos", "We’re open"),
    ("La casa de Juan Llorens", "At Juan Llorens"),
    ("En Juan Llorens 18. Cortes, barba y tratamientos de piel en el barrio de La Petxina.",
     "At Juan Llorens 18. Haircuts, beard work and skin treatments in La Petxina."),
    ("La tienda del Carmen, en la calle Baja. Cortes, degradados y barba con Camilo, Dani y el criterio de la casa.",
     "The Carmen shop on Calle Baja. Cuts, fades and beard work with Camilo, Dani and the house standard."),
    ("Silueta de", "Silhouette of"),
    ("Aquí irá su foto.", "Photo coming soon."),
    # Services page
    ("La carta, tienda por tienda", "The menu, shop by shop"),
    ("Cada servicio lleva su precio. «Reserva aquí» abre la carta de esa tienda en Booksy. Al lado, el mismo servicio por WhatsApp.",
     "Each service shows its price. “Book here” opens that shop’s Booksy menu. Next to it, the same service on WhatsApp."),
    ("Booksy El Carmen", "Booksy El Carmen"),
    ("Booksy La Petxina", "Booksy La Petxina"),
    # Contact
    ("Escríbenos", "Write to us"),
    ("Sugerencias, dudas o elogios. El mensaje se prepara para info@barbershopvalencia.com.",
     "Suggestions, questions or compliments. The message is prepared for info@barbershopvalencia.com."),
    ("Correo", "Email"),
    ("Nombre", "Name"),
    ("Teléfono", "Phone"),
    ("Tipo de mensaje", "Message type"),
    ("Sugerencia", "Suggestion"),
    ("Duda", "Question"),
    ("Elogio", "Compliment"),
    ("Mensaje", "Message"),
    ("Cuéntanos tu sugerencia, duda o elogio", "Tell us your suggestion, question or compliment"),
    ("Enviar", "Send"),
    # Service names / common terms
    ("Corte clásico / degradado", "Classic cut / fade"),
    ("Corte clásico", "Classic cut"),
    ("Corte skin fade", "Skin fade"),
    ("Corte a tijera VIP", "VIP scissor cut"),
    ("Corte VIP", "VIP cut"),
    ("Corte + arreglo de barba", "Cut + beard trim"),
    ("Corte + barba VIP", "Cut + VIP beard"),
    ("Corte + barba jubilado", "Cut + beard (senior)"),
    ("Corte + cejas", "Cut + eyebrows"),
    ("Corte a tijera", "Scissor cut"),
    ("Corte de niño", "Kids cut"),
    ("Corte niño solo tijera", "Kids scissor-only cut"),
    ("Corte jubilados", "Senior cut"),
    ("Corte con diseño", "Design cut"),
    ("Afeitado de cabeza + barba", "Head shave + beard"),
    ("Afeitado completo de cabeza", "Full head shave"),
    ("Afeitado completo de barba", "Full beard shave"),
    ("Afeitado de barba completo", "Full beard shave"),
    ("Arreglo de barba express", "Express beard trim"),
    ("Barba VIP", "VIP beard"),
    ("Marcar líneas", "Line up"),
    ("Marcado de líneas", "Line up"),
    ("Rapado", "Buzz cut"),
    ("Dibujos", "Designs"),
    ("Cejas", "Eyebrows"),
    ("Exfoliación", "Exfoliation"),
    ("Mascarilla carbón activo", "Activated charcoal mask"),
    ("Limpieza facial de arcilla", "Clay facial cleanse"),
    ("Full: corte + barba + cejas", "Full: cut + beard + eyebrows"),
    ("El corte de casa en La Petxina, con lavado opcional.", "The house cut at La Petxina, with optional wash."),
    ("Degradado al cero, el más pedido en El Carmen.", "Zero fade, the most requested at El Carmen."),
    ("Pelo y barba en la misma cita, en cualquiera de las dos tiendas.", "Hair and beard in the same visit, at either shop."),
    ("Perfilado con más tiempo y un acabado más cuidado.", "Shaping with more time and a more refined finish."),
    ("Diseño a cuchilla o navaja para cerrar el look.", "Blade or razor design to finish the look."),
    ("Mascarilla de arcilla en La Petxina.", "Clay mask at La Petxina."),
    ("Máquina en los lados y tijera arriba.", "Clippers on the sides and scissors on top."),
    # Titles / meta (Spanish → English)
    ("Barbería en Valencia con dos tiendas", "Barbershop in Valencia with two shops"),
    ("Barbería El Carmen", "El Carmen Barbershop"),
    ("Barbería La Petxina", "La Petxina Barbershop"),
    ("Servicios y precios", "Services and prices"),
    ("Carta de cortes, barba y tratamientos", "Menu of cuts, beard work and treatments"),
    ("Contacta Barber Shop Valencia", "Contact Barber Shop Valencia"),
    ("Sugerencias, dudas o reserva.", "Suggestions, questions or bookings."),
    ("Redes sociales", "Social networks"),
    ("Carrusel de marcas", "Brand carousel"),
    # Blog
    ("Blog", "Blog"),
    ("Estilo y barbería en Valencia", "Style and barbershop tips in Valencia"),
    ("Consejos de cortes, barba y reserva. Los últimos artículos de Barber Shop Valencia.",
     "Haircut, beard and booking tips. The latest articles from Barber Shop Valencia."),
    ("Dos locales, barberos expertos y reserva online.",
     "Two shops, expert barbers and online booking."),
    ("Barbería con cita previa en Valencia", "Barbershop appointments in Valencia"),
    ("Reserva online y llega a tu hora, sin esperas.",
     "Book online and arrive on time — no waiting."),
    ("Ver todo el blog", "See all blog posts"),
    ("Barbería en Valencia: estilo masculino y servicio profesional",
     "Barbershop in Valencia: men's style and professional service"),
    ("6 de octubre de 2026", "6 October 2026"),
    ("3 de octubre de 2026", "3 October 2026"),
    ("./blog/9-octubre-valencia-barberia-abierta-la-petxina.html",
     "./blog/9-october-valencia-barbershop-open-la-petxina.html"),
    ("./blog/barberia-en-valencia.html", "./blog/barbershop-in-valencia.html"),
    ("./blog/barberia-cita-previa-valencia.html", "./blog/appointment-barbershop-valencia.html"),
    ("9 de octubre en Valencia: La Petxina abierta",
     "9 October in Valencia: La Petxina open"),
    ("Feriado del Nou d’Octubre: qué hacer, cortes para celebrar y reserva en La Petxina. El Carmen cerrado.",
     "Nou d’Octubre holiday: what to do, celebration cuts and booking at La Petxina. El Carmen closed."),
    ("8 de octubre de 2026", "8 October 2026"),
    ('alt="9 de octubre en Barber Shop Valencia"', 'alt="9 October at Barber Shop Valencia"'),
    ('alt="Zona de trabajo Barber Shop Valencia"', 'alt="Work area at Barber Shop Valencia"'),
    ('alt="Interior Barber Shop Valencia"', 'alt="Interior of Barber Shop Valencia"'),
]


def rewrite_asset_paths(html: str) -> str:
    html = html.replace('href="assets/', 'href="../assets/')
    html = html.replace('src="assets/', 'src="../assets/')
    html = html.replace('href="site.webmanifest"', 'href="../site.webmanifest"')
    for name in PAGE_MAP_ES_TO_EN:
        html = re.sub(rf'href="{re.escape(name)}"', f'href="./{name}"', html)
        html = re.sub(rf'href="{re.escape(name)}#', f'href="./{name}#', html)
    return html


def fix_seo_base(html: str, lang: str, page: str) -> str:
    # Normalize any previous base then set language path
    html = html.replace(f"{BASE}/es/", f"{BASE}/")
    html = html.replace(f"{BASE}/en/", f"{BASE}/")
    # Point page URLs to /{lang}/...
    html = html.replace(f'href="{BASE}/"', f'href="{BASE}/{lang}/"')
    html = html.replace(f'content="{BASE}/"', f'content="{BASE}/{lang}/"')
    for es_name, en_name in PAGE_MAP_ES_TO_EN.items():
        target = en_name if lang == "en" else es_name
        html = html.replace(f"{BASE}/{es_name}", f"{BASE}/{lang}/{target}")
        if es_name != en_name:
            html = html.replace(f"{BASE}/{en_name}", f"{BASE}/{lang}/{target}")
    # Keep shared assets at root
    html = html.replace(f"{BASE}/{lang}/assets/", f"{BASE}/assets/")
    # Canonical for index
    if page in ("index.html",):
        html = re.sub(
            r'<link rel="canonical" href="[^"]*">',
            f'<link rel="canonical" href="{BASE}/{lang}/">',
            html,
            count=1,
        )
        html = html.replace(f'og:url" content="{BASE}/{lang}/index.html"', f'og:url" content="{BASE}/{lang}/"')
    return html


def add_hreflang(html: str, lang: str, es_page: str) -> str:
    en_page = PAGE_MAP_ES_TO_EN[es_page]
    es_href = f"{BASE}/es/" if es_page == "index.html" else f"{BASE}/es/{es_page}"
    en_href = f"{BASE}/en/" if en_page == "index.html" else f"{BASE}/en/{en_page}"
    block = (
        f'  <link rel="alternate" hreflang="es" href="{es_href}">\n'
        f'  <link rel="alternate" hreflang="en" href="{en_href}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{es_href}">\n'
    )
    html = re.sub(r'  <link rel="alternate" hreflang="[^"]+" href="[^"]*">\n', "", html)
    html = html.replace('<link rel="canonical"', block + "  <link rel=\"canonical\"", 1)
    return html


def add_lang_switch(html: str, lang: str, es_page: str) -> str:
    en_page = PAGE_MAP_ES_TO_EN[es_page]
    es_href = f"./{es_page}" if lang == "es" else f"../es/{es_page}"
    en_href = f"./{en_page}" if lang == "en" else f"../en/{en_page}"
    es_cls = ' class="is-active"' if lang == "es" else ""
    en_cls = ' class="is-active"' if lang == "en" else ""
    label = "Language" if lang == "en" else "Idioma"
    switch = (
        f'      <div class="lang" aria-label="{label}">\n'
        f'        <a{es_cls} href="{es_href}" hreflang="es">ES</a>\n'
        f'        <a{en_cls} href="{en_href}" hreflang="en">EN</a>\n'
        f'      </div>\n'
    )
    html = re.sub(r'      <div class="lang"[\s\S]*?</div>\n', "", html)
    # Insert before first ghost/primary booking button in nav
    for marker in (
        '<a class="btn btn--ghost" href="#reservar">',
        '<a class="btn btn--ghost" href="https://booksy.com',
        '<a class="btn btn--primary" href="https://api.whatsapp.com',
    ):
        if marker in html:
            html = html.replace(marker, switch + "      " + marker, 1)
            break
    return html



def ensure_blog_nav(html: str, lang: str) -> str:
    """Keep a single Blog link after Servicios/Services."""
    # Drop duplicates in main nav first
    html = re.sub(r'(\n\s*<a href="\./blog/"[^>]*>Blog</a>)+', '\n      <a href="./blog/">Blog</a>', html)
    nav_m = re.search(r'<nav class="nav__links"[^>]*>(.*?)</nav>', html, re.S)
    if nav_m and 'href="./blog/"' in nav_m.group(1):
        return html
    if lang == "es":
        return re.sub(
            r'(<a href="\./servicios\.html"[^>]*>Servicios</a>)',
            r'\1\n      <a href="./blog/">Blog</a>',
            html,
            count=1,
        )
    return re.sub(
        r'(<a href="\./services\.html"[^>]*>Services</a>)',
        r'\1\n      <a href="./blog/">Blog</a>',
        html,
        count=1,
    )


def translate_to_en(html: str) -> str:
    html = html.replace('lang="es"', 'lang="en"', 1)
    for src, dst in EN_REPLACEMENTS:
        html = html.replace(src, dst)
    # Nav services/contact filenames
    html = html.replace('href="./servicios.html"', 'href="./services.html"')
    html = html.replace('href="./contacto.html"', 'href="./contact.html"')
    html = html.replace('href="servicios.html"', 'href="./services.html"')
    html = html.replace('href="contacto.html"', 'href="./contact.html"')
    # WhatsApp prefilled Spanish greetings → English
    html = html.replace(
        "Hola%2C%20quiero%20reservar",
        "Hi%2C%20I%20want%20to%20book",
    )
    html = html.replace(
        "Hola%2C%20quiero%20reservar%20una%20cita%20en",
        "Hi%2C%20I%20want%20to%20book%20an%20appointment%20at",
    )
    html = html.replace("%20en%20Barber%20Shop%20Valencia", "%20at%20Barber%20Shop%20Valencia")
    # Schema language
    html = html.replace('"inLanguage": "es-ES"', '"inLanguage": "en-GB"')
    html = html.replace("Comunidad Valenciana", "Valencian Community")
    html = html.replace('"España"', '"Spain"')
    # Breadcrumb labels already partly translated via replacements
    html = html.replace('"name": "Inicio"', '"name": "Home"')
    html = html.replace('"name": "Servicios"', '"name": "Services"')
    html = html.replace('"name": "Contacto"', '"name": "Contact"')
    return html


def build() -> None:
    sources = {
        "index.html": (ROOT / "es" / "index.html").read_text(),
        "el-carmen.html": (ROOT / "es" / "el-carmen.html").read_text(),
        "la-petxina.html": (ROOT / "es" / "la-petxina.html").read_text(),
        "servicios.html": (ROOT / "es" / "servicios.html").read_text(),
        "contacto.html": (ROOT / "es" / "contacto.html").read_text(),
    }
    # Strip ../ from asset paths in es sources before rewrite
    sources = {
        k: v.replace('href="../assets/', 'href="assets/').replace('src="../assets/', 'src="assets/').replace('href="../site.webmanifest"', 'href="site.webmanifest"')
        for k, v in sources.items()
    }

    es_dir = ROOT / "es"
    en_dir = ROOT / "en"
    es_dir.mkdir(exist_ok=True)
    en_dir.mkdir(exist_ok=True)

    for es_name, content in sources.items():
        # Spanish
        es_html = rewrite_asset_paths(content)
        es_html = fix_seo_base(es_html, "es", es_name)
        es_html = add_hreflang(es_html, "es", es_name)
        es_html = add_lang_switch(es_html, "es", es_name)
        es_html = ensure_blog_nav(es_html, "es")
        (es_dir / es_name).write_text(es_html)

        # English
        en_name = PAGE_MAP_ES_TO_EN[es_name]
        en_html = rewrite_asset_paths(content)
        # Rename internal ES filenames before SEO rewrite
        en_html = en_html.replace("servicios.html", "services.html")
        en_html = en_html.replace("contacto.html", "contact.html")
        en_html = translate_to_en(en_html)
        en_html = fix_seo_base(en_html, "en", en_name)
        # Fix SEO page names that still say servicios/contacto after translate
        en_html = en_html.replace(f"{BASE}/en/servicios.html", f"{BASE}/en/services.html")
        en_html = en_html.replace(f"{BASE}/en/contacto.html", f"{BASE}/en/contact.html")
        en_html = add_hreflang(en_html, "en", es_name)
        en_html = add_lang_switch(en_html, "en", es_name)
        en_html = ensure_blog_nav(en_html, "en")
        (en_dir / en_name).write_text(en_html)
        print(f"ok es/{es_name} + en/{en_name}")

    # Root redirect by domain (always refresh)
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
  <link rel="alternate" hreflang="x-default" href="{BASE}/es/">
  <link rel="canonical" href="{BASE}/es/">
  <meta http-equiv="refresh" content="0; url=es/">
  <script>
    // .com and .es both open Spanish by default; English via /en/ or the ES|EN switcher
    location.replace("es/");
  </script>
</head>
<body>
  <p><a href="es/">Español</a> · <a href="en/">English</a></p>
</body>
</html>
"""
    )

    # Sitemap both languages (+ blog)
    from datetime import date

    today = date.today().isoformat()
    urls = []
    for lang, pages in {
        "es": list(PAGE_MAP_ES_TO_EN.keys()),
        "en": list(PAGE_MAP_ES_TO_EN.values()),
    }.items():
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

    blog_pages = {
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
    }
    for lang, pages in blog_pages.items():
        for page in pages:
            loc = f"{BASE}/{lang}/blog/" if page == "index.html" else f"{BASE}/{lang}/blog/{page}"
            priority = "0.85" if page == "index.html" else "0.8"
            urls.append(
                f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>"""
            )

    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n"
    )

    # Lang switch CSS snippet append if missing
    css = (ROOT / "assets" / "style.css").read_text()
    if ".lang {" not in css:
        css += """

.lang {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.lang a {
  color: rgba(247, 246, 243, 0.55);
  border: 1px solid #3a3a36;
  padding: 0.35rem 0.5rem;
}

.lang a.is-active,
.lang a:hover {
  color: var(--gold);
  border-color: var(--gold);
}
"""
        (ROOT / "assets" / "style.css").write_text(css)

    print("done")


if __name__ == "__main__":
    build()
