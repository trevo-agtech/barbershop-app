#!/usr/bin/env python3
"""Generate ES/EN blog index + 4 latest posts (SEO-optimized, local images)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://barbershopvalencia.es"

FOOTER_ES = """<footer class="footer">
    <div class="container footer__grid">
      <div>
        <h3>Barber Shop Valencia</h3>
        <p>Dos barberías en Valencia. Cortes, barba y cuidado masculino con el sello de Miguel y su equipo.</p>
        <div class="socials" aria-label="Redes sociales">
        <a href="https://www.instagram.com/barbershopvalencia_/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4zm5 4.2A4.8 4.8 0 1 0 16.8 12 4.8 4.8 0 0 0 12 7.2zm6.3-.8a1.15 1.15 0 1 0 1.15 1.15A1.15 1.15 0 0 0 18.3 6.4zM12 9.1A2.9 2.9 0 1 1 9.1 12 2.9 2.9 0 0 1 12 9.1z"/></svg></a>
        <a href="https://www.tiktok.com/search?q=Barber%20Shop%20Valencia" target="_blank" rel="noopener" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.2 3h2.3a5.2 5.2 0 0 0 3.4 3.2v2.3a7.4 7.4 0 0 1-3.4-1.1v7.1a6 6 0 1 1-6-6c.3 0 .7 0 1 .1v2.5a3.5 3.5 0 1 0 2.5 3.4V3z"/></svg></a>
        <a href="https://www.facebook.com/barbershop.valencia.9" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.2 8.5H17V5.4h-2.8c-2.3 0-4.1 1.8-4.1 4.1v2H8v3.1h2.1V21h3.2v-6.4h2.7l.4-3.1h-3.1v-1.6c0-.7.4-1.4 1.4-1.4z"/></svg></a>
        <a href="https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia" target="_blank" rel="noopener" aria-label="Booksy"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2.8h2.1V5h5.8V2.8H17V5h1.6A2.4 2.4 0 0 1 21 7.4V19a2.4 2.4 0 0 1-2.4 2.4H5.4A2.4 2.4 0 0 1 3 19V7.4A2.4 2.4 0 0 1 5.4 5H7zm12 7.2H5v9h14z"/></svg></a>
      </div>
      </div>
      <div>
        <h3>La Petxina</h3>
        <address>
          <p><a href="https://www.google.com/maps/search/?api=1&query=C%2F+Juan+Llorens+18%2C+46008+Valencia%2C+Espa%C3%B1a" target="_blank" rel="noopener">C/ Juan Llorens 18<br>46008 Valencia, España</a></p>
        </address>
      </div>
      <div>
        <h3>El Carmen</h3>
        <address>
          <p><a href="https://www.google.com/maps/search/?api=1&query=C%2F+Baja+50%2C+46008+Valencia%2C+Espa%C3%B1a" target="_blank" rel="noopener">C/ Baja, 50<br>46008 Valencia, España</a></p>
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

FOOTER_EN = FOOTER_ES.replace("Dos barberías en Valencia. Cortes, barba y cuidado masculino con el sello de Miguel y su equipo.", "Two barbershops in Valencia. Haircuts, beard work and men's grooming with Miguel and his team.").replace('aria-label="Redes sociales"', 'aria-label="Social networks"').replace("España", "Spain").replace('aria-label="WhatsApp"', 'aria-label="WhatsApp"')


def nav(lang: str, active: str = "blog") -> str:
    if lang == "es":
        home, shops, elc, pet, svc, blog, contact = (
            "../index.html",
            "../index.html#tiendas",
            "../el-carmen.html",
            "../la-petxina.html",
            "../servicios.html",
            "./index.html",
            "../contacto.html",
        )
        labels = ("Inicio", "Nuestras tiendas", "Servicios", "Blog", "Contacto", "Idioma", "Abrir menú")
        en_blog = "../../en/blog/index.html"
        es_blog = "./index.html"
    else:
        home, shops, elc, pet, svc, blog, contact = (
            "../index.html",
            "../index.html#tiendas",
            "../el-carmen.html",
            "../la-petxina.html",
            "../services.html",
            "./index.html",
            "../contact.html",
        )
        labels = ("Home", "Our shops", "Services", "Blog", "Contact", "Language", "Open menu")
        en_blog = "./index.html"
        es_blog = "../../es/blog/index.html"

    def act(name: str) -> str:
        return ' class="is-active"' if active == name else ""

    return f"""<header class="nav">
    <a class="nav__brand" href="{home}"><img src="../../assets/logo-bw-transparent.png" alt="Barber Shop Valencia" width="56" height="62">Barber Shop Valencia</a>
    <button class="nav__toggle" type="button" data-nav-toggle aria-expanded="false" aria-label="{labels[6]}"><span></span></button>
    <nav class="nav__links" data-nav>
      <a href="{home}"{act("home")}>{labels[0]}</a>
      <div class="nav__drop">
        <a href="{shops}" data-drop-toggle aria-expanded="false">{labels[1]}</a>
        <ul class="dropdown">
          <li><a href="{elc}">El Carmen</a></li>
          <li><a href="{pet}">La Petxina</a></li>
        </ul>
      </div>
      <a href="{svc}"{act("servicios")}>{labels[2]}</a>
      <a href="{blog}"{act("blog")}>{labels[3]}</a>
      <a href="{contact}"{act("contacto")}>{labels[4]}</a>
      <div class="lang" aria-label="{labels[5]}">
        <a{(' class="is-active"' if lang == "es" else "")} href="{es_blog}" hreflang="es">ES</a>
        <a{(' class="is-active"' if lang == "en" else "")} href="{en_blog}" hreflang="en">EN</a>
      </div>
      <a class="btn btn--ghost" href="https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia" target="_blank" rel="noopener">Booksy</a>
      <a class="btn btn--primary" href="https://api.whatsapp.com/send/?phone=34677142958&text&type=phone_number&app_absent=0" target="_blank" rel="noopener">WhatsApp</a>
    </nav>
  </header>
"""


POSTS = [
    {
        "es_slug": "barberia-en-valencia.html",
        "en_slug": "barbershop-in-valencia.html",
        "date": "2026-10-06",
        "date_label_es": "6 de octubre de 2026",
        "date_label_en": "6 October 2026",
        "image": "IMG_0860.jpg",
        "image_alt_es": "Interior de Barber Shop Valencia en El Carmen",
        "image_alt_en": "Interior of Barber Shop Valencia in El Carmen",
        "title_es": "Barbería en Valencia: estilo masculino y servicio profesional",
        "title_en": "Barbershop in Valencia: men's style and professional service",
        "desc_es": "Buscas una barbería en Valencia con cortes modernos, barba y reserva fácil? Descubre Barber Shop Valencia en El Carmen y La Petxina.",
        "desc_en": "Looking for a barbershop in Valencia with modern cuts, beard work and easy booking? Discover Barber Shop Valencia in El Carmen and La Petxina.",
        "excerpt_es": "Dos locales en Valencia, barberos expertos y reserva online. Así es la experiencia Barber Shop Valencia.",
        "excerpt_en": "Two shops in Valencia, expert barbers and online booking. This is the Barber Shop Valencia experience.",
        "body_es": """
        <p>Si buscas una <strong>barbería en Valencia</strong> que combine calidad, experiencia y atención personalizada, Barber Shop Valencia es tu opción. Con dos locales —El Carmen (C/ Baja 50) y La Petxina (C/ Juan Llorens 18)— ofrecemos cortes modernos, cuidado de barba y tratamientos en un ambiente profesional y relajado.</p>
        <h2>Qué nos diferencia como barbería en Valencia</h2>
        <ul>
          <li>Ubicaciones céntricas: El Carmen y La Petxina.</li>
          <li>Equipo de barberos con criterio y detalle en cada acabado.</li>
          <li>Reserva online en Booksy o por WhatsApp, sin complicaciones.</li>
          <li>Productos premium para cabello y barba.</li>
          <li>Mismo horario en ambas tiendas: lunes a viernes 10:00–20:00, sábado 10:00–18:00 y domingo 11:00–17:00.</li>
        </ul>
        <h2>Servicios que más piden en Valencia</h2>
        <h3>Cortes modernos y clásicos</h3>
        <p>Desde fades personalizados hasta cortes clásicos con degradado. Te asesoramos según tu rostro, tipo de cabello y estilo de vida para que el resultado se note fuera de la silla.</p>
        <h3>Cuidado de barba</h3>
        <p>Perfilado con precisión, hidratación y afeitado tradicional. Un servicio pensado para mantener la barba definida entre visitas.</p>
        <h3>Tratamientos faciales</h3>
        <p>Exfoliación, hidratación y limpieza adaptada a la piel del hombre. Ideal si quieres una imagen cuidada sin complicar tu rutina.</p>
        <h2>Dónde encontrarnos</h2>
        <p><a href="../el-carmen.html">Barber Shop Valencia El Carmen</a> — C/ Baja 50, 46008 Valencia.<br>
        <a href="../la-petxina.html">Barber Shop Valencia La Petxina</a> — C/ Juan Llorens 18, 46008 Valencia.</p>
        <p>Consulta la <a href="../servicios.html">carta de servicios</a> o reserva ya tu cita.</p>
        """,
        "body_en": """
        <p>If you want a <strong>barbershop in Valencia</strong> with quality, experience and personal attention, Barber Shop Valencia is for you. With two locations —El Carmen (C/ Baja 50) and La Petxina (C/ Juan Llorens 18)— we offer modern cuts, beard care and treatments in a professional, relaxed setting.</p>
        <h2>What sets our Valencia barbershop apart</h2>
        <ul>
          <li>Central locations: El Carmen and La Petxina.</li>
          <li>Barbers focused on clean finishes and real advice.</li>
          <li>Book online on Booksy or WhatsApp — no hassle.</li>
          <li>Premium products for hair and beard.</li>
          <li>Same hours in both shops: Mon–Fri 10:00–20:00, Sat 10:00–18:00, Sun 11:00–17:00.</li>
        </ul>
        <h2>Services men book most in Valencia</h2>
        <h3>Modern and classic cuts</h3>
        <p>From custom fades to classic tapered cuts. We advise based on your face shape, hair type and lifestyle so the result holds up outside the chair.</p>
        <h3>Beard care</h3>
        <p>Precise shaping, hydration and traditional shaves — built to keep your beard sharp between visits.</p>
        <h3>Facial treatments</h3>
        <p>Exfoliation, hydration and cleansing tailored for men's skin — a fresh look without a complicated routine.</p>
        <h2>Where to find us</h2>
        <p><a href="../el-carmen.html">Barber Shop Valencia El Carmen</a> — C/ Baja 50, 46008 Valencia.<br>
        <a href="../la-petxina.html">Barber Shop Valencia La Petxina</a> — C/ Juan Llorens 18, 46008 Valencia.</p>
        <p>See our <a href="../services.html">services menu</a> or book your appointment now.</p>
        """,
    },
    {
        "es_slug": "barberia-cita-previa-valencia.html",
        "en_slug": "appointment-barbershop-valencia.html",
        "date": "2026-10-03",
        "date_label_es": "3 de octubre de 2026",
        "date_label_en": "3 October 2026",
        "image": "IMG_0834.jpg",
        "image_alt_es": "Sillón y zona de trabajo en Barber Shop Valencia",
        "image_alt_en": "Chair and work area at Barber Shop Valencia",
        "title_es": "Barbería con cita previa en Valencia: tu estilo, sin esperas",
        "title_en": "Barbershop with appointment in Valencia: your style, no waiting",
        "desc_es": "Reserva en una barbería con cita previa en Valencia. Cortes, barba y tratamientos en El Carmen o La Petxina por Booksy o WhatsApp.",
        "desc_en": "Book a barbershop appointment in Valencia. Haircuts, beard and treatments in El Carmen or La Petxina via Booksy or WhatsApp.",
        "excerpt_es": "Reserva online, llega a tu hora y sal con el corte listo. Así funciona nuestra cita previa en Valencia.",
        "excerpt_en": "Book online, arrive on time and leave with a sharp cut. How appointments work at our Valencia shops.",
        "body_es": """
        <p>En Barber Shop Valencia sabemos que tu tiempo importa. Por eso ofrecemos <strong>barbería con cita previa en Valencia</strong>: llegas, te sentamos y trabajamos tu corte o barba sin colas innecesarias.</p>
        <h2>Por qué reservar con cita previa</h2>
        <ul>
          <li>Sin esperas largas: llegas a tu hora y te atendemos.</li>
          <li>Atención personalizada en cortes, barbas y tratamientos.</li>
          <li>Ambiente profesional en El Carmen y La Petxina.</li>
          <li>Reserva en minutos desde Booksy o WhatsApp.</li>
        </ul>
        <h2>Cómo reservar en 3 pasos</h2>
        <ol>
          <li>Elige local: <a href="../el-carmen.html">El Carmen</a> o <a href="../la-petxina.html">La Petxina</a>.</li>
          <li>Selecciona servicio (corte, barba, combo o tratamiento) en <a href="../servicios.html">nuestra carta</a>.</li>
          <li>Confirma horario en Booksy o escríbenos por WhatsApp.</li>
        </ol>
        <h2>Servicios que puedes reservar</h2>
        <h3>Corte de pelo para hombre</h3>
        <p>Estilos modernos y clásicos adaptados a tu rostro. El equipo está en formación continua para aplicar tendencias con criterio.</p>
        <h3>Barba y afeitado</h3>
        <p>Desde el perfilado con navaja hasta tratamientos con aceites. Un cuidado completo para mantener la barba impecable.</p>
        <h3>Tratamientos faciales</h3>
        <p>Limpieza, exfoliación e hidratación pensadas para la piel masculina.</p>
        <h2>Reserva ahora</h2>
        <p>Elige tu local favorito y asegura tu hueco. También puedes escribirnos a <a href="mailto:info@barbershopvalencia.com">info@barbershopvalencia.com</a> o al WhatsApp +34 677 142 958.</p>
        """,
        "body_en": """
        <p>At Barber Shop Valencia your time matters. That is why we offer a <strong>barbershop with appointments in Valencia</strong>: you arrive, sit down, and we work on your cut or beard without unnecessary queues.</p>
        <h2>Why book ahead</h2>
        <ul>
          <li>No long waits: arrive at your slot and we take you in.</li>
          <li>Personal attention for cuts, beards and treatments.</li>
          <li>Professional setting in El Carmen and La Petxina.</li>
          <li>Book in minutes on Booksy or WhatsApp.</li>
        </ul>
        <h2>How to book in 3 steps</h2>
        <ol>
          <li>Choose a shop: <a href="../el-carmen.html">El Carmen</a> or <a href="../la-petxina.html">La Petxina</a>.</li>
          <li>Pick a service (cut, beard, combo or treatment) from our <a href="../services.html">menu</a>.</li>
          <li>Confirm a time on Booksy or message us on WhatsApp.</li>
        </ol>
        <h2>Services you can book</h2>
        <h3>Men's haircut</h3>
        <p>Modern and classic styles adapted to your face. The team keeps training so trends are applied with judgment.</p>
        <h3>Beard and shave</h3>
        <p>From razor line-ups to oil treatments — full care to keep your beard sharp.</p>
        <h3>Facial treatments</h3>
        <p>Cleansing, exfoliation and hydration designed for men's skin.</p>
        <h2>Book now</h2>
        <p>Pick your preferred shop and lock in a slot. You can also email <a href="mailto:info@barbershopvalencia.com">info@barbershopvalencia.com</a> or WhatsApp +34 677 142 958.</p>
        """,
    },
    {
        "es_slug": "corte-pelo-hombre-valencia.html",
        "en_slug": "mens-haircut-valencia.html",
        "date": "2026-09-28",
        "date_label_es": "28 de septiembre de 2026",
        "date_label_en": "28 September 2026",
        "image": "IMG_0858.jpg",
        "image_alt_es": "Detalle del local Barber Shop Valencia listo para un corte",
        "image_alt_en": "Barber Shop Valencia shop detail ready for a haircut",
        "title_es": "Corte de pelo hombre en Valencia: guía práctica 2026",
        "title_en": "Men's haircut in Valencia: practical 2026 guide",
        "desc_es": "Corte de pelo para hombre en Valencia: fades, crop, clásicos y barba. Reserva en El Carmen o La Petxina con Barber Shop Valencia.",
        "desc_en": "Men's haircut in Valencia: fades, crop, classics and beard. Book in El Carmen or La Petxina at Barber Shop Valencia.",
        "excerpt_es": "Qué pedir en la silla, cuánto dura un corte y cómo mantenerlo entre visitas en Valencia.",
        "excerpt_en": "What to ask for in the chair, how long a cut takes, and how to keep it sharp between visits in Valencia.",
        "body_es": """
        <p>Si buscas un <strong>corte de pelo hombre en Valencia</strong> con estilo, calidad y asesoramiento real, en Barber Shop Valencia trabajamos tendencias actuales y técnicas clásicas en El Carmen y La Petxina.</p>
        <h2>Por qué elegirnos para tu corte</h2>
        <ul>
          <li>Barberos que adaptan el corte a tu rostro y tipo de cabello.</li>
          <li>Ambiente cómodo en dos barrios bien conectados.</li>
          <li>Productos de calidad para que el acabado dure más.</li>
          <li>Reserva online o por WhatsApp cuando te venga bien.</li>
        </ul>
        <h2>Estilos que más pedimos en 2026</h2>
        <ul>
          <li><strong>Fade / skin fade:</strong> limpio, versátil y fácil de mantener.</li>
          <li><strong>Crop texturizado:</strong> natural, moderno y con movimiento.</li>
          <li><strong>Undercut actualizado:</strong> laterales cortos con volumen controlado arriba.</li>
          <li><strong>Clásico con degradado:</strong> elegante para oficina y fin de semana.</li>
        </ul>
        <h2>Preguntas frecuentes</h2>
        <h3>¿Hace falta cita previa?</h3>
        <p>Recomendamos reservar para asegurar horario. También atendemos sin cita según disponibilidad.</p>
        <h3>¿Cuánto dura un corte?</h3>
        <p>Unos 30 minutos de media; puede variar según el estilo y si añades barba.</p>
        <h3>¿Hacéis barba y anticaída?</h3>
        <p>Sí: perfilado, afeitado y tratamientos capilares. Mira la <a href="../servicios.html">carta completa</a>.</p>
        <h3>¿Cada cuánto retoque?</h3>
        <p>Cada 3–4 semanas suele ser el ritmo ideal para mantener líneas y volumen.</p>
        <h2>Reserva tu corte en Valencia</h2>
        <p>Elige <a href="../el-carmen.html">El Carmen</a> o <a href="../la-petxina.html">La Petxina</a> y reserva tu hueco. Si dudas entre estilos, en la silla te orientamos con honestidad.</p>
        """,
        "body_en": """
        <p>If you want a <strong>men's haircut in Valencia</strong> with style, quality and honest advice, Barber Shop Valencia delivers current trends and classic technique in El Carmen and La Petxina.</p>
        <h2>Why book your cut with us</h2>
        <ul>
          <li>Barbers who adapt the cut to your face and hair type.</li>
          <li>Comfortable shops in two well-connected neighbourhoods.</li>
          <li>Quality products so the finish lasts longer.</li>
          <li>Book online or on WhatsApp when it suits you.</li>
        </ul>
        <h2>Styles we cut most in 2026</h2>
        <ul>
          <li><strong>Fade / skin fade:</strong> clean, versatile and easy to maintain.</li>
          <li><strong>Textured crop:</strong> natural, modern, with movement.</li>
          <li><strong>Updated undercut:</strong> short sides with controlled volume on top.</li>
          <li><strong>Classic taper:</strong> sharp for the office and the weekend.</li>
        </ul>
        <h2>FAQ</h2>
        <h3>Do I need an appointment?</h3>
        <p>We recommend booking to secure a slot. Walk-ins are welcome when there is availability.</p>
        <h3>How long does a haircut take?</h3>
        <p>About 30 minutes on average; longer if you add a beard service.</p>
        <h3>Do you offer beard work and anti-hair-loss treatments?</h3>
        <p>Yes — line-ups, shaves and scalp treatments. See the <a href="../services.html">full menu</a>.</p>
        <h3>How often should I come back?</h3>
        <p>Every 3–4 weeks is usually ideal to keep lines and shape sharp.</p>
        <h2>Book your haircut in Valencia</h2>
        <p>Choose <a href="../el-carmen.html">El Carmen</a> or <a href="../la-petxina.html">La Petxina</a> and lock in a time. Unsure about the style? We will guide you in the chair.</p>
        """,
    },
    {
        "es_slug": "mejor-barberia-valencia.html",
        "en_slug": "best-barbershop-valencia.html",
        "date": "2026-09-22",
        "date_label_es": "22 de septiembre de 2026",
        "date_label_en": "22 September 2026",
        "image": "IMG_0820.jpg",
        "image_alt_es": "Ambiente de Barber Shop Valencia, barbería en Valencia",
        "image_alt_en": "Atmosphere at Barber Shop Valencia barbershop",
        "title_es": "Mejor barbería en Valencia: por qué eligen Barber Shop Valencia",
        "title_en": "Best barbershop in Valencia: why men choose Barber Shop Valencia",
        "desc_es": "Descubre por qué muchos buscan la mejor barbería en Valencia en Barber Shop Valencia: cortes, barba, ambiente y dos locales céntricos.",
        "desc_en": "See why men looking for the best barbershop in Valencia choose Barber Shop Valencia: cuts, beard, atmosphere and two central shops.",
        "excerpt_es": "Criterio en el corte, ambiente cuidado y dos direcciones fáciles en Valencia. Lo que nos piden al buscar “la mejor barbería”.",
        "excerpt_en": "Judgment in the cut, a cared-for space and two easy addresses in Valencia — what men want when they search “best barbershop”.",
        "body_es": """
        <p>Cuando alguien busca la <strong>mejor barbería en Valencia</strong>, no solo mira el precio: mira el acabado, el trato y si el local merece la visita. En Barber Shop Valencia unimos profesionalismo, detalle y atención personalizada en cada silla.</p>
        <h2>Razones por las que vuelven</h2>
        <h3>Equipo actualizado</h3>
        <p>Barberos formados en técnicas modernas y clásicas. El objetivo no es copiar una foto: es que el corte te favorezca de verdad.</p>
        <h3>Ambiente pensado para ti</h3>
        <p>Espacios cómodos en El Carmen y La Petxina, con ritmo de trabajo serio pero sin prisas de fábrica.</p>
        <h3>Atención individual</h3>
        <p>Desde el asesoramiento inicial hasta el último perfilado. Cada detalle cuenta.</p>
        <h3>Productos premium</h3>
        <p>Usamos productos de calidad para cabello y barba, pensados para que el resultado se mantenga entre visitas.</p>
        <h2>Servicios que nos diferencian</h2>
        <ul>
          <li>Cortes modernos y clásicos: fades, undercuts, crop y más.</li>
          <li>Cuidado integral de barba: perfilado, aceites y bálsamos.</li>
          <li>Afeitado tradicional con técnica profesional.</li>
          <li>Tratamientos capilares e hidratación.</li>
          <li>Tratamientos faciales masculinos.</li>
          <li>Asesoramiento para elegir el estilo que encaja contigo.</li>
        </ul>
        <h2>FAQ rápida</h2>
        <p><strong>¿Cita previa?</strong> Recomendada; también según disponibilidad.<br>
        <strong>¿Duración de un corte?</strong> En torno a 30 minutos.<br>
        <strong>¿Pagos?</strong> Efectivo, tarjeta y pagos digitales.<br>
        <strong>¿Eventos?</strong> Podemos preparar cortes para bodas, sesiones o fechas especiales.</p>
        <h2>Ven a conocernos</h2>
        <p>Reserva en <a href="../el-carmen.html">El Carmen (C/ Baja 50)</a> o en <a href="../la-petxina.html">La Petxina (C/ Juan Llorens 18)</a>. Si quieres ver el día a día, síguenos en Instagram <a href="https://www.instagram.com/barbershopvalencia_/" target="_blank" rel="noopener">@barbershopvalencia_</a>.</p>
        """,
        "body_en": """
        <p>When someone searches for the <strong>best barbershop in Valencia</strong>, price is not the only factor: finish, service and whether the shop is worth the visit matter. At Barber Shop Valencia we combine craft, detail and personal attention in every chair.</p>
        <h2>Why clients come back</h2>
        <h3>A sharp team</h3>
        <p>Barbers trained in modern and classic techniques. The goal is not to copy a photo — it is a cut that actually suits you.</p>
        <h3>A space built for you</h3>
        <p>Comfortable shops in El Carmen and La Petxina, with a serious pace but no factory rush.</p>
        <h3>Individual attention</h3>
        <p>From the first recommendation to the last line-up. Every detail counts.</p>
        <h3>Premium products</h3>
        <p>Quality products for hair and beard so results hold between visits.</p>
        <h2>Services that set us apart</h2>
        <ul>
          <li>Modern and classic cuts: fades, undercuts, crop and more.</li>
          <li>Full beard care: shaping, oils and balms.</li>
          <li>Traditional shaves with professional technique.</li>
          <li>Scalp treatments and hydration.</li>
          <li>Men's facial treatments.</li>
          <li>Advice to choose a style that fits you.</li>
        </ul>
        <h2>Quick FAQ</h2>
        <p><strong>Appointment?</strong> Recommended; walk-ins when available.<br>
        <strong>Cut duration?</strong> Around 30 minutes.<br>
        <strong>Payments?</strong> Cash, card and digital payments.<br>
        <strong>Events?</strong> We can prep cuts for weddings, shoots or special dates.</p>
        <h2>Come see us</h2>
        <p>Book at <a href="../el-carmen.html">El Carmen (C/ Baja 50)</a> or <a href="../la-petxina.html">La Petxina (C/ Juan Llorens 18)</a>. For day-to-day work, follow us on Instagram <a href="https://www.instagram.com/barbershopvalencia_/" target="_blank" rel="noopener">@barbershopvalencia_</a>.</p>
        """,
    },
]


def head(
    *,
    lang: str,
    title: str,
    description: str,
    canonical: str,
    hreflang_es: str,
    hreflang_en: str,
    og_image: str,
    article: dict | None = None,
) -> str:
    locale = "es_ES" if lang == "es" else "en_GB"
    schema = ""
    if article:
        schema = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{article['title']}",
    "description": "{description}",
    "image": "{og_image}",
    "datePublished": "{article['date']}",
    "dateModified": "{article['date']}",
    "author": {{ "@type": "Organization", "name": "Barber Shop Valencia" }},
    "publisher": {{
      "@type": "Organization",
      "name": "Barber Shop Valencia",
      "logo": {{ "@type": "ImageObject", "url": "{BASE}/assets/logo-bw.png" }}
    }},
    "mainEntityOfPage": "{canonical}",
    "inLanguage": "{"es-ES" if lang == "es" else "en-GB"}"
  }}
  </script>"""
    else:
        schema = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Blog",
    "name": "{title}",
    "description": "{description}",
    "url": "{canonical}",
    "inLanguage": "{"es-ES" if lang == "es" else "en-GB"}",
    "publisher": {{ "@type": "Organization", "name": "Barber Shop Valencia" }}
  }}
  </script>"""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Barber Shop Valencia</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <link rel="alternate" hreflang="es" href="{hreflang_es}">
  <link rel="alternate" hreflang="en" href="{hreflang_en}">
  <link rel="alternate" hreflang="x-default" href="{hreflang_es}">
  <link rel="canonical" href="{canonical}">
  <meta name="geo.region" content="ES-VC">
  <meta name="geo.placename" content="Valencia">
  <meta property="og:type" content="{"article" if article else "website"}">
  <meta property="og:locale" content="{locale}">
  <meta property="og:site_name" content="Barber Shop Valencia">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
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


def write_index(lang: str) -> None:
    is_es = lang == "es"
    title = "Blog de barbería en Valencia" if is_es else "Barbershop blog in Valencia"
    desc = (
        "Consejos de cortes, barba y estilo masculino en Valencia. Artículos de Barber Shop Valencia en El Carmen y La Petxina."
        if is_es
        else "Haircut, beard and men's style tips in Valencia. Articles from Barber Shop Valencia in El Carmen and La Petxina."
    )
    can = f"{BASE}/{lang}/blog/"
    html = head(
        lang=lang,
        title=title,
        description=desc,
        canonical=can,
        hreflang_es=f"{BASE}/es/blog/",
        hreflang_en=f"{BASE}/en/blog/",
        og_image=f"{BASE}/assets/el-carmen/web/IMG_0860.jpg",
    )
    html += nav(lang, "blog")
    label = "Blog" if is_es else "Blog"
    lead = (
        "Tendencias, consejos y novedades de Barber Shop Valencia. Cortes, barba y estilo en El Carmen y La Petxina."
        if is_es
        else "Trends, tips and news from Barber Shop Valencia. Cuts, beard and style in El Carmen and La Petxina."
    )
    read = "Leer artículo" if is_es else "Read article"
    html += f"""
  <section class="section blog-hero">
    <div class="container">
      <p class="section__label">{label}</p>
      <h1 class="section__title">{title}</h1>
      <p class="section__lead">{lead}</p>
    </div>
  </section>
  <section class="section section--alt">
    <div class="container blog-grid">
"""
    for p in POSTS:
        slug = p["es_slug"] if is_es else p["en_slug"]
        ptitle = p["title_es"] if is_es else p["title_en"]
        excerpt = p["excerpt_es"] if is_es else p["excerpt_en"]
        date_l = p["date_label_es"] if is_es else p["date_label_en"]
        alt = p["image_alt_es"] if is_es else p["image_alt_en"]
        html += f"""
      <article class="blog-card">
        <a class="blog-card__media" href="./{slug}">
          <img src="../../assets/el-carmen/web/{p['image']}" alt="{alt}" width="1200" height="900" loading="lazy">
        </a>
        <div class="blog-card__body">
          <time datetime="{p['date']}">{date_l}</time>
          <h2><a href="./{slug}">{ptitle}</a></h2>
          <p>{excerpt}</p>
          <a class="btn btn--ghost btn--sm" href="./{slug}">{read}</a>
        </div>
      </article>
"""
    html += """
    </div>
  </section>
"""
    html += FOOTER_ES if is_es else FOOTER_EN
    out = ROOT / lang / "blog" / "index.html"
    out.write_text(html)
    print("ok", out.relative_to(ROOT))


def write_post(lang: str, p: dict) -> None:
    is_es = lang == "es"
    slug = p["es_slug"] if is_es else p["en_slug"]
    other = p["en_slug"] if is_es else p["es_slug"]
    title = p["title_es"] if is_es else p["title_en"]
    desc = p["desc_es"] if is_es else p["desc_en"]
    body = p["body_es"] if is_es else p["body_en"]
    date_l = p["date_label_es"] if is_es else p["date_label_en"]
    alt = p["image_alt_es"] if is_es else p["image_alt_en"]
    can = f"{BASE}/{lang}/blog/{slug}"
    es_href = f"{BASE}/es/blog/{p['es_slug']}"
    en_href = f"{BASE}/en/blog/{p['en_slug']}"
    og = f"{BASE}/assets/el-carmen/web/{p['image']}"
    html = head(
        lang=lang,
        title=title,
        description=desc,
        canonical=can,
        hreflang_es=es_href,
        hreflang_en=en_href,
        og_image=og,
        article={"title": title, "date": p["date"]},
    )
    # Fix lang switcher for post pages
    n = nav(lang, "blog")
    if is_es:
        n = n.replace('href="./index.html" hreflang="es"', f'href="./{slug}" hreflang="es"')
        n = n.replace('href="../../en/blog/index.html" hreflang="en"', f'href="../../en/blog/{other}" hreflang="en"')
    else:
        n = n.replace('href="./index.html" hreflang="en"', f'href="./{slug}" hreflang="en"')
        n = n.replace('href="../../es/blog/index.html" hreflang="es"', f'href="../../es/blog/{other}" hreflang="es"')
    html += n
    back = "← Volver al blog" if is_es else "← Back to blog"
    cta_title = "Reserva tu cita" if is_es else "Book your appointment"
    cta_text = (
        "Elige El Carmen o La Petxina y reserva por Booksy o WhatsApp."
        if is_es
        else "Choose El Carmen or La Petxina and book on Booksy or WhatsApp."
    )
    book_el = "Reservar El Carmen" if is_es else "Book El Carmen"
    book_pet = "Reservar La Petxina" if is_es else "Book La Petxina"
    html += f"""
  <article class="section blog-post">
    <div class="container blog-post__wrap">
      <p class="blog-post__back"><a href="./index.html">{back}</a></p>
      <header class="blog-post__header">
        <p class="section__label">Blog</p>
        <h1 class="section__title">{title}</h1>
        <time datetime="{p['date']}">{date_l}</time>
      </header>
      <figure class="blog-post__hero">
        <img src="../../assets/el-carmen/web/{p['image']}" alt="{alt}" width="1600" height="1200">
      </figure>
      <div class="blog-post__content prose">
        {body}
      </div>
      <div class="blog-post__cta">
        <h2>{cta_title}</h2>
        <p>{cta_text}</p>
        <div class="cta__actions cta__actions--stack">
          <a class="btn btn--primary" href="https://booksy.com/es-es/132769_barber-shop-valencia-el-carmen_barberia_58087_valencia" target="_blank" rel="noopener">{book_el}</a>
          <a class="btn btn--ghost" href="https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia" target="_blank" rel="noopener">{book_pet}</a>
          <a class="btn btn--ghost" href="https://api.whatsapp.com/send/?phone=34677142958&text&type=phone_number&app_absent=0" target="_blank" rel="noopener">WhatsApp</a>
        </div>
      </div>
    </div>
  </article>
"""
    html += FOOTER_ES if is_es else FOOTER_EN
    out = ROOT / lang / "blog" / slug
    out.write_text(html)
    print("ok", out.relative_to(ROOT))


def patch_main_nav() -> None:
    """Insert Blog link after Servicios/Services on main es/en pages."""
    import re

    patterns = {
        "es": (
            r'(<a href="\./servicios\.html"[^>]*>Servicios</a>)',
            r'\1\n      <a href="./blog/">Blog</a>',
        ),
        "en": (
            r'(<a href="\./services\.html"[^>]*>Services</a>)',
            r'\1\n      <a href="./blog/">Blog</a>',
        ),
    }
    for folder, (pat, repl) in patterns.items():
        for path in (ROOT / folder).glob("*.html"):
            html = path.read_text()
            if 'href="./blog/"' in html:
                continue
            html2, n = re.subn(pat, repl, html, count=1)
            if n:
                path.write_text(html2)
                print("nav", path.relative_to(ROOT))


def main() -> None:
    for lang in ("es", "en"):
        (ROOT / lang / "blog").mkdir(parents=True, exist_ok=True)
        write_index(lang)
        for p in POSTS:
            write_post(lang, p)
    patch_main_nav()
    print("done")


if __name__ == "__main__":
    main()
