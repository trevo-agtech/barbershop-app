(function () {
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll("[data-drop-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      if (window.matchMedia("(max-width: 899px)").matches) {
        event.preventDefault();
        var item = btn.closest(".nav__drop");
        var open = item.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      }
    });
  });

  var header = document.querySelector(".nav");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  var lightbox = document.querySelector("[data-lightbox]");
  if (lightbox) {
    var img = lightbox.querySelector("img");
    var caption = lightbox.querySelector("[data-lightbox-caption]");
    var close = function () {
      lightbox.hidden = true;
      document.body.classList.remove("is-locked");
    };
    document.querySelectorAll("[data-gallery] img").forEach(function (photo) {
      photo.addEventListener("click", function () {
        img.src = photo.currentSrc || photo.src;
        img.alt = photo.alt;
        if (caption) caption.textContent = photo.alt;
        lightbox.hidden = false;
        document.body.classList.add("is-locked");
      });
    });
    lightbox.addEventListener("click", function (event) {
      if (event.target === lightbox || event.target.closest("[data-lightbox-close]")) close();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !lightbox.hidden) close();
    });
  }

  var form = document.querySelector("[data-contact-form]");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var tipo = data.get("tipo");
      var nombre = String(data.get("nombre") || "").trim();
      var email = String(data.get("email") || "").trim();
      var telefono = String(data.get("telefono") || "").trim();
      var mensaje = String(data.get("mensaje") || "").trim();
      var subject = encodeURIComponent("[" + tipo + "] Barber Shop Valencia — " + nombre);
      var body = encodeURIComponent(
        "Tipo: " + tipo + "\n" +
        "Nombre: " + nombre + "\n" +
        "Email: " + email + "\n" +
        "Teléfono: " + telefono + "\n\n" +
        mensaje
      );
      trackEvent("submit_contact", {
        form_type: String(tipo || "contacto"),
        page_path: location.pathname
      });
      window.location.href = "mailto:info@barbershopvalencia.com?subject=" + subject + "&body=" + body;
      var note = form.querySelector("[data-form-note]");
      if (note) {
        note.hidden = false;
        note.textContent = "Se abrió tu correo para enviar el mensaje a info@barbershopvalencia.com.";
      }
    });
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest("a");
    if (!link) return;
    var href = link.getAttribute("href") || "";
    if (!href || href.charAt(0) === "#") {
      if (!/^#(reservar|tiendas)\b/i.test(href)) return;
    }
    var label = linkLabel(link);
    var whatsapp = /whatsapp\.com|wa\.me/i.test(href);
    var booksy = /booksy\.com/i.test(href);
    var reservar = isReserveCta(href, label);
    if (!whatsapp && !booksy && !reservar) return;

    var params = {
      link_text: label,
      shop: shopFrom(href, label),
      placement: placementOf(link),
      page_path: location.pathname,
      language: document.documentElement.lang || ""
    };
    if (whatsapp) {
      trackEvent("click_whatsapp", params);
      if (params.shop === "el_carmen") trackEvent("click_whatsapp_el_carmen", params);
      if (params.shop === "la_petxina") trackEvent("click_whatsapp_la_petxina", params);
    }
    if (booksy) {
      trackEvent("click_booksy", params);
      if (params.shop === "el_carmen") trackEvent("click_booksy_el_carmen", params);
      if (params.shop === "la_petxina") trackEvent("click_booksy_la_petxina", params);
    }
    if (reservar) {
      params.channel = whatsapp ? "whatsapp" : booksy ? "booksy" : "page";
      trackEvent("click_reservar", params);
    }
  });

  function linkLabel(link) {
    var text = (link.textContent || "").replace(/\s+/g, " ").trim();
    if (text) return text;
    return (link.getAttribute("aria-label") || "").replace(/\s+/g, " ").trim();
  }

  function isReserveCta(href, label) {
    if (/^#(reservar|tiendas)\b/i.test(href)) return true;
    if (!label || /^booksy$/i.test(label)) return false;
    return /reserv|\bbook\b|запис/i.test(label);
  }

  function shopFrom(href, label) {
    var hay = (href + " " + label).toLowerCase();
    var carmen = /el[- ]carmen|132769|34634456940/.test(hay);
    var petxinaLink = /petxina|12979/.test(hay);
    var defaultWhatsapp = /34677142958/.test(hay) && !petxinaLink;
    if (carmen && !petxinaLink) return "el_carmen";
    if (petxinaLink && !carmen) return "la_petxina";
    if (defaultWhatsapp) {
      if (/\/la-petxina(?:\.html|\/|$)/i.test(location.pathname)) return "la_petxina";
      if (/\/el-carmen(?:\.html|\/|$)/i.test(location.pathname)) return "el_carmen";
      return "general";
    }
    if (/\/el-carmen(?:\.html|\/|$)/i.test(location.pathname)) return "el_carmen";
    if (/\/la-petxina(?:\.html|\/|$)/i.test(location.pathname)) return "la_petxina";
    return "general";
  }

  function placementOf(link) {
    if (link.classList.contains("wa")) return "floating";
    if (link.closest(".nav, header")) return "header";
    if (link.closest("footer, .footer")) return "footer";
    if (link.closest("#reservar, .cta")) return "cta";
    if (link.closest(".service, .service__actions")) return "service";
    if (link.closest(".hero")) return "hero";
    if (link.closest(".hw-modal, .hw-ribbon, .hw-chip")) return "halloween";
    return "content";
  }

  function trackEvent(name, params) {
    if (typeof window.gtag !== "function") return;
    var payload = { transport_type: "beacon" };
    Object.keys(params).forEach(function (key) {
      if (params[key] == null || params[key] === "") return;
      payload[key] = String(params[key]).slice(0, 100);
    });
    window.gtag("event", name, payload);
  }
})();

/* Oferta de Halloween até 31 oct 2026 (Europe/Madrid). O desconto vale de 26 a 31. Fora do período não altera a página. */
(function () {
  var START = "2026-10-24";
  var END = "2026-10-31";
  var STORAGE = "bsv-halloween-2026";
  var today = madridDateKey(new Date());
  if (today < START || today > END) {
    document.querySelectorAll("[data-halloween-seo]").forEach(function (node) {
      node.remove();
    });
    return;
  }

  var modal = null;
  var lastFocus = null;
  var copy = null;

  function madridDateKey(date) {
    try {
      return new Intl.DateTimeFormat("en-CA", {
        timeZone: "Europe/Madrid",
        year: "numeric",
        month: "2-digit",
        day: "2-digit"
      }).format(date);
    } catch (error) {
      return date.toISOString().slice(0, 10);
    }
  }

  function readDismissed() {
    try { return sessionStorage.getItem(STORAGE) === "1"; } catch (error) { return false; }
  }

  function rememberDismissed() {
    try { sessionStorage.setItem(STORAGE, "1"); } catch (error) {}
  }

  function decorations() {
    var wrap = document.createElement("div");
    wrap.className = "hw-decor";
    wrap.setAttribute("aria-hidden", "true");
    wrap.innerHTML =
      web("hw-web hw-web--tl") +
      web("hw-web hw-web--tr") +
      bat("hw-bat hw-bat--1") +
      bat("hw-bat hw-bat--2") +
      bat("hw-bat hw-bat--3") +
      '<span class="hw-float hw-float--pumpkin hw-float--a">' + pumpkin() + "</span>" +
      '<span class="hw-float hw-float--skull hw-float--b">' + skull() + "</span>" +
      '<span class="hw-float hw-float--pumpkin hw-float--c">' + pumpkin() + "</span>" +
      '<span class="hw-float hw-float--skull hw-float--d">' + skull() + "</span>";
    return wrap;
  }

  function web(className) {
    return '<svg class="' + className + '" viewBox="0 0 100 100" focusable="false">' +
      '<g fill="none" stroke="currentColor" stroke-width="0.7">' +
      '<path d="M0 0 L100 0 M0 0 L100 28 M0 0 L100 58 M0 0 L100 100 M0 0 L58 100 M0 0 L22 100 M0 0 L0 100"/>' +
      '<path d="M20 0 C30 12 12 24 0 18 M40 0 C58 20 24 46 0 38 M62 0 C86 30 38 68 0 58 M84 10 C104 50 54 90 8 82"/>' +
      "</g></svg>";
  }

  function bat(className) {
    return '<span class="' + className + '"><svg viewBox="0 0 64 32" focusable="false">' +
      '<path d="M32 14c2-6 6-9 10-8 1 4-1 7-3 9 4 1 8 0 12-2-1 4-4 6-8 7 3 2 5 5 5 8-4-1-7-3-9-6-1 4-3 7-7 8 0-4 1-7 3-10-2 3-3 6-3 10-4-1-6-4-7-8-2 3-5 5-9 6 0-3 2-6 5-8-4-1-7-3-8-7 4 2 8 3 12 2-2-2-4-5-3-9 4-1 8 2 10 8z"/>' +
      "</svg></span>";
  }

  function pumpkin() {
    return '<span class="hw-ico hw-ico--pumpkin"><svg viewBox="0 0 64 72" focusable="false">' +
      '<path fill="#2f7a34" d="M34.2 16.5c.2-6.4 2.4-10.6 4.6-12.2-.2 4.6-2.6 7.4-4.8 8.6 1.8.6 3.4 1.6 4 3.2-2.2.8-4.2.6-5.6.2.4 1.6.8 2.2 1.8 2.2z"/>' +
      '<path fill="#67b85a" d="M30.4 15.2c2.2-1.2 5.4-1 7.2.4-2.2 1.4-5.2 1.6-7.2-.4z"/>' +
      '<ellipse cx="18.5" cy="44" rx="11" ry="16.5" fill="#e15a12"/>' +
      '<ellipse cx="45.5" cy="44" rx="11" ry="16.5" fill="#e15a12"/>' +
      '<ellipse cx="32" cy="43.5" rx="15" ry="19.5" fill="#ff9a22" stroke="#9a3d0c" stroke-width="1.6"/>' +
      '<path d="M32 25.5c-.6 8-.4 20 .2 34" fill="none" stroke="#e15a12" stroke-width="1.7" stroke-linecap="round"/>' +
      '<ellipse cx="26.5" cy="36" rx="3.2" ry="6" fill="#ffd089" opacity=".8"/>' +
      '<ellipse cx="25.5" cy="42" rx="2.3" ry="3" fill="#4a2412"/>' +
      '<ellipse cx="38.5" cy="42" rx="2.3" ry="3" fill="#4a2412"/>' +
      '<circle cx="24.8" cy="41.2" r=".7" fill="#fff6ea"/>' +
      '<circle cx="37.8" cy="41.2" r=".7" fill="#fff6ea"/>' +
      '<path d="M26.5 49.5c1.8 2.6 9.2 2.6 11 0" fill="none" stroke="#4a2412" stroke-width="1.8" stroke-linecap="round"/>' +
      '<ellipse cx="21.5" cy="47.5" rx="2.1" ry="1.15" fill="#ff7a86" opacity=".7"/>' +
      '<ellipse cx="42.5" cy="47.5" rx="2.1" ry="1.15" fill="#ff7a86" opacity=".7"/>' +
      "</svg></span>";
  }

  function skull() {
    return '<span class="hw-ico hw-ico--skull"><svg viewBox="0 0 64 72" focusable="false">' +
      '<path fill="#fff8ee" stroke="#3a2a22" stroke-width="1.6" stroke-linejoin="round" d="M32 7c-13.2 0-22 10.4-22 23.2 0 8.8 4.2 15.8 10.2 19.4l.4 8.2c.2 2.2 2 3.8 4.2 3.8h4.4V52.2h5.6V61.6h4.4c2.2 0 4-1.6 4.2-3.8l.4-8.2C49.8 46 54 39 54 30.2 54 17.4 45.2 7 32 7z"/>' +
      '<ellipse cx="23" cy="30" rx="5.4" ry="6.2" fill="#2c211c"/>' +
      '<ellipse cx="41" cy="30" rx="5.4" ry="6.2" fill="#2c211c"/>' +
      '<circle cx="21.2" cy="28.2" r="1.5" fill="#fff8ee"/>' +
      '<circle cx="39.2" cy="28.2" r="1.5" fill="#fff8ee"/>' +
      '<path fill="#2c211c" d="M32 37.2l-2.8 4.4h5.6z"/>' +
      '<path d="M24.5 48.5h15" fill="none" stroke="#2c211c" stroke-width="1.5" stroke-linecap="round"/>' +
      '<path d="M27 48.5v6.2M32 48.5v6.8M37 48.5v6.2" fill="none" stroke="#2c211c" stroke-width="1.35" stroke-linecap="round"/>' +
      '<ellipse cx="16.5" cy="36" rx="2" ry="1.1" fill="#ffb4b8" opacity=".85"/>' +
      '<ellipse cx="47.5" cy="36" rx="2" ry="1.1" fill="#ffb4b8" opacity=".85"/>' +
      "</svg></span>";
  }

  function ribbon() {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "hw-ribbon";
    button.innerHTML = pumpkin() + '<span class="hw-ribbon__text">' + copy.ribbon + '</span><span class="hw-ribbon__date">' + copy.ribbonDate + "</span>" + skull();
    button.addEventListener("click", openModal);
    return button;
  }

  function syncHalloweenBar(bar) {
    var apply = function () {
      var nav = document.querySelector(".nav");
      var height = bar.offsetHeight || 0;
      document.documentElement.style.setProperty("--hw-bar", height + "px");
      document.documentElement.style.setProperty("--hw-stack", (height + (nav ? nav.offsetHeight : 0)) + "px");
    };
    apply();
    window.addEventListener("resize", apply);
  }

  function chip() {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "hw-chip";
    button.setAttribute("aria-label", copy.chipLabel);
    button.textContent = "10%";
    button.addEventListener("click", openModal);
    return button;
  }

  function buildModal() {
    var root = document.createElement("div");
    root.className = "hw-modal";
    root.hidden = true;
    root.innerHTML =
      '<div class="hw-modal__backdrop" data-hw-close></div>' +
      '<div class="hw-modal__panel" role="dialog" aria-modal="true" aria-labelledby="hw-title">' +
        '<button class="hw-modal__close" type="button" data-hw-close aria-label="' + copy.close + '">×</button>' +
        '<p class="hw-modal__kicker">' + pumpkin() + "<span>" + copy.kicker + "</span>" + skull() + "</p>" +
        '<h2 id="hw-title">' + copy.title + "</h2>" +
        '<p class="hw-modal__offer"><strong>10%</strong><span>' + copy.lead + "</span></p>" +
        "<p class=\"hw-modal__note\">" + copy.note + "</p>" +
        '<div class="hw-shops">' + shop("El Carmen", copy.waCarmen, BOOKS.carmen) + shop("La Petxina", copy.waPetxina, BOOKS.petxina) + "</div>" +
        '<p class="hw-modal__fine">' + copy.fine + "</p>" +
      "</div>";
    root.addEventListener("click", function (event) {
      if (event.target.closest("[data-hw-close]")) closeModal();
    });
    document.addEventListener("keydown", onKeydown);
    return root;
  }

  function shop(name, whatsapp, booksy) {
    return '<section class="hw-shop"><h3>' + name + "</h3>" +
      '<div class="hw-shop__actions">' +
        '<a class="btn btn--primary btn--sm" href="' + booksy + '" target="_blank" rel="noopener">Booksy</a>' +
        '<a class="btn btn--ghost btn--sm" href="' + whatsapp + '" target="_blank" rel="noopener">WhatsApp</a>' +
      "</div></section>";
  }

  function openModal() {
    if (!modal || !modal.hidden) return;
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.classList.add("is-locked");
    var close = modal.querySelector(".hw-modal__close");
    if (close) close.focus();
  }

  function closeModal() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove("is-locked");
    rememberDismissed();
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  function onKeydown(event) {
    if (!modal || modal.hidden) return;
    if (event.key === "Escape") {
      event.preventDefault();
      closeModal();
      return;
    }
    if (event.key !== "Tab") return;
    var items = modal.querySelectorAll("a, button");
    if (!items.length) return;
    var first = items[0];
    var last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  var BOOKS = {
    carmen: "https://booksy.com/es-es/132769_barber-shop-valencia-el-carmen_barberia_58087_valencia",
    petxina: "https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia"
  };

  function wa(phone, text) {
    return "https://api.whatsapp.com/send/?phone=" + phone + "&text=" + encodeURIComponent(text) + "&type=phone_number&app_absent=0";
  }

  var COPY = {
    es: {
      ribbon: "Halloween · 10% nuevos clientes",
      ribbonDate: "26–31 oct",
      chipLabel: "Ver la oferta de Halloween, 10% para nuevos clientes",
      close: "Cerrar",
      kicker: "Del 26 al 31 de octubre",
      title: "Oferta fantasmagórica",
      lead: "Para nuevos clientes, en cualquier corte de pelo.",
      note: "Agenda por Booksy o por WhatsApp. Al reservar, di que eres cliente nuevo.",
      fine: "Válido del 26 al 31 de octubre de 2026. Un uso por persona. No acumulable con otras promociones.",
      waCarmen: wa("34634456940", "Hola, soy cliente nuevo y quiero la oferta fantasmagórica de Halloween: 10% en un corte en Barber Shop Valencia El Carmen."),
      waPetxina: wa("34677142958", "Hola, soy cliente nuevo y quiero la oferta fantasmagórica de Halloween: 10% en un corte en Barber Shop Valencia La Petxina.")
    },
    en: {
      ribbon: "Halloween · 10% for new clients",
      ribbonDate: "26–31 Oct",
      chipLabel: "See the Halloween offer, 10% for new clients",
      close: "Close",
      kicker: "26–31 October",
      title: "Ghostly offer",
      lead: "For new clients, on any haircut.",
      note: "Book on Booksy or WhatsApp. When you book, say you are a new client.",
      fine: "Valid 26–31 October 2026. One use per person. Not combinable with other offers.",
      waCarmen: wa("34634456940", "Hi, I'm a new client and I want the Halloween ghostly offer: 10% off a haircut at Barber Shop Valencia El Carmen."),
      waPetxina: wa("34677142958", "Hi, I'm a new client and I want the Halloween ghostly offer: 10% off a haircut at Barber Shop Valencia La Petxina.")
    },
    ru: {
      ribbon: "Хэллоуин · 10% новым клиентам",
      ribbonDate: "26–31 окт",
      chipLabel: "Смотреть предложение на Хэллоуин, 10% для новых клиентов",
      close: "Закрыть",
      kicker: "С 26 по 31 октября",
      title: "Призрачное предложение",
      lead: "Новым клиентам на любую стрижку.",
      note: "Запишитесь через Booksy или WhatsApp и скажите, что вы новый клиент.",
      fine: "Действует с 26 по 31 октября 2026. Один раз на человека. Не суммируется с другими акциями.",
      waCarmen: wa("34634456940", "Здравствуйте, я новый клиент и хочу призрачное предложение на Хэллоуин: скидка 10% на стрижку в Barber Shop Valencia El Carmen."),
      waPetxina: wa("34677142958", "Здравствуйте, я новый клиент и хочу призрачное предложение на Хэллоуин: скидка 10% на стрижку в Barber Shop Valencia La Petxina.")
    }
  };

  var lang = (document.documentElement.lang || "es").slice(0, 2);
  copy = COPY[lang] || COPY.es;

  document.body.classList.add("is-halloween");
  document.body.appendChild(decorations());
  var bar = ribbon();
  document.body.appendChild(bar);
  syncHalloweenBar(bar);
  document.body.appendChild(chip());
  modal = buildModal();
  document.body.appendChild(modal);

  if (!readDismissed()) window.setTimeout(openModal, 400);
})();
