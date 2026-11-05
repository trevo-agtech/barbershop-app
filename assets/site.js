(function () {
  var host = location.hostname.toLowerCase();
  var path = location.pathname.replace(/index\.html$/i, "");
  if (host === "barbershopvalencia.com" || host === "www.barbershopvalencia.com" || host === "www.barbershopvalencia.es") {
    location.replace("https://barbershopvalencia.es" + path + location.search + location.hash);
    return;
  }
  if (/index\.html$/i.test(location.pathname)) {
    location.replace(path + location.search + location.hash);
    return;
  }

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

  mountBlackWeek();
  stampOutboundLinks();

  document.addEventListener("click", function (event) {
    var link = event.target.closest("a");
    if (!link) return;
    stampLink(link);
    var href = link.getAttribute("href") || "";
    if (!href || href.charAt(0) === "#") {
      if (!/^#(reservar|tiendas)\b/i.test(href)) return;
    }
    var label = linkLabel(link);
    var channel = channelOf(href);
    var reservar = isReserveCta(href, label);
    if (!channel && !reservar) return;

    var params = trackingParams(link, href, label, channel);
    trackEvent("click_outbound", params);
    if (channel === "whatsapp") {
      trackEvent("click_whatsapp", params);
      if (params.shop === "el_carmen") trackEvent("click_whatsapp_el_carmen", params);
      if (params.shop === "la_petxina") trackEvent("click_whatsapp_la_petxina", params);
    }
    if (channel === "booksy") {
      trackEvent("click_booksy", params);
      if (params.shop === "el_carmen") trackEvent("click_booksy_el_carmen", params);
      if (params.shop === "la_petxina") trackEvent("click_booksy_la_petxina", params);
    }
    if (channel === "instagram") trackEvent("click_instagram", params);
    if (channel === "facebook") trackEvent("click_facebook", params);
    if (channel === "tiktok") trackEvent("click_tiktok", params);
    if (channel === "maps") trackEvent("click_maps", params);
    if (channel === "email") trackEvent("click_email", params);
    if (reservar) {
      params.channel = channel || "page";
      trackEvent("click_reservar", params);
    }
  });

  function stampOutboundLinks() {
    document.querySelectorAll("a[href]").forEach(stampLink);
  }

  function stampLink(link) {
    if (link.dataset.utmReady === "1") return;
    var href = link.getAttribute("href") || "";
    var channel = channelOf(href);
    if (!channel || /^mailto:/i.test(href)) {
      if (channel) link.dataset.utc = utcCode(link, href, channel);
      if (channel) link.dataset.utmReady = "1";
      return;
    }
    var label = linkLabel(link);
    var placement = placementOf(link);
    var shop = shopFrom(href, label);
    var lang = languageCode();
    var utc = [channel, shop, placement, lang].join("_");
    try {
      var url = new URL(href, location.href);
      if (!url.searchParams.has("utm_source")) {
        url.searchParams.set("utm_source", "website");
        url.searchParams.set("utm_medium", placement);
        url.searchParams.set("utm_campaign", channel);
        url.searchParams.set("utm_content", shop);
        url.searchParams.set("utm_term", pageCode());
        url.searchParams.set("utc", utc);
        link.setAttribute("href", url.toString());
      }
    } catch (error) {}
    link.dataset.utc = utc;
    link.dataset.utmReady = "1";
  }

  function trackingParams(link, href, label, channel) {
    return {
      link_text: label,
      link_url: href,
      shop: shopFrom(href, label),
      placement: placementOf(link),
      page_path: location.pathname,
      language: languageCode(),
      utm_source: "website",
      utm_medium: placementOf(link),
      utm_campaign: channel || "reservar",
      utm_content: shopFrom(href, label),
      utm_term: pageCode(),
      utc: link.dataset.utc || utcCode(link, href, channel || "reservar")
    };
  }

  function utcCode(link, href, channel) {
    return [channel, shopFrom(href, linkLabel(link)), placementOf(link), languageCode()].join("_");
  }

  function channelOf(href) {
    if (/booksy\.com/i.test(href)) return "booksy";
    if (/whatsapp\.com|wa\.me/i.test(href)) return "whatsapp";
    if (/instagram\.com/i.test(href)) return "instagram";
    if (/facebook\.com|fb\.com/i.test(href)) return "facebook";
    if (/tiktok\.com/i.test(href)) return "tiktok";
    if (/google\.com\/maps|maps\.google|goo\.gl\/maps/i.test(href)) return "maps";
    if (/^mailto:/i.test(href)) return "email";
    return "";
  }

  function languageCode() {
    return (document.documentElement.lang || "es").slice(0, 2).toLowerCase();
  }

  function pageCode() {
    var path = location.pathname.replace(/\/index\.html$/i, "/").replace(/\.html$/i, "");
    var parts = path.split("/").filter(Boolean);
    return (parts.join("_") || "home").slice(0, 80);
  }

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
    var clean = String(href || "").replace(/[?&](?:utm_[a-z]+|utc)=[^&#]*/gi, "");
    var hay = (clean + " " + label).toLowerCase();
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
    if (/juan(?:\s|\+|%20)*llorens/.test(hay)) return "la_petxina";
    if (/google\.com\/maps|maps\.google/.test(hay) && /baja/.test(hay)) return "el_carmen";
    if (/\/el-carmen(?:\.html|\/|$)/i.test(location.pathname)) return "el_carmen";
    if (/\/la-petxina(?:\.html|\/|$)/i.test(location.pathname)) return "la_petxina";
    return "general";
  }

  function placementOf(link) {
    if (link.classList.contains("wa")) return "floating";
    if (link.closest(".nav, header")) return "header";
    if (link.closest("footer, .footer")) return "footer";
    if (link.closest("#reservar, .cta, .bf-bar, .bf-deals")) return "cta";
    if (link.closest(".service, .service__actions")) return "service";
    if (link.closest(".hero")) return "hero";
    return "content";
  }

  function mountBlackWeek() {
    if (!blackWeekOpen()) {
      restoreBlackWeekCopy();
      return;
    }
    document.body.classList.add("is-blackweek");
    var lang = languageCode();
    var copy = blackWeekCopy();
    var t = copy[lang] || copy.es;
    var petxina = "https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia";
    var bar = document.createElement("div");
    bar.className = "bf-bar";
    bar.innerHTML =
      '<div class="bf-bar__inner container">' +
        '<p class="bf-bar__copy"><strong>' + t.kicker + '</strong>' +
        '<span class="bf-bar__dates">' + t.dates + '</span>' +
        '<span>' + t.text + '</span></p>' +
        '<div class="bf-bar__actions">' +
          '<a class="btn btn--primary btn--sm" href="' + petxina + '" target="_blank" rel="noopener">' + t.book + '</a>' +
        '</div></div>';
    document.body.insertBefore(bar, document.body.firstChild);
    function fitBar() {
      document.body.style.setProperty("--bf-h", bar.offsetHeight + "px");
    }
    fitBar();
    window.addEventListener("resize", fitBar);
    document.querySelectorAll(".services").forEach(function (list) {
      var note = document.createElement("p");
      note.className = "bf-price-note";
      note.textContent = t.note;
      list.parentNode.insertBefore(note, list);
    });
    document.querySelectorAll(".service__price").forEach(function (price) {
      var service = price.closest(".service");
      if (!service || !isPetxinaFullCut(service)) return;
      var match = price.textContent.match(/(\d+)(?:[.,](\d+))?\s*€/);
      if (!match) return;
      var cents = parseInt(match[1], 10) * 100 + (match[2] ? parseInt((match[2] + "00").slice(0, 2), 10) : 0);
      price.innerHTML =
        '<span class="service__price-old">' + formatCents(cents) + '</span>' +
        '<span class="service__price-now service__price-now--flash">20 €</span>' +
        '<span class="service__flash">' + t.flash + '</span>';
    });
  }

  function blackWeekOpen() {
    var day;
    try {
      day = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Madrid", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
    } catch (error) {
      day = new Date().toISOString().slice(0, 10);
    }
    return day <= "2026-11-29";
  }

  function restoreBlackWeekCopy() {
    document.querySelectorAll("[data-bf-restore]").forEach(function (el) {
      if (el.tagName === "META") el.setAttribute("content", el.getAttribute("data-bf-restore"));
      else el.textContent = el.getAttribute("data-bf-restore");
    });
    document.querySelectorAll("[data-bf-restore-href]").forEach(function (el) {
      el.setAttribute("href", el.getAttribute("data-bf-restore-href"));
      if ((el.getAttribute("href") || "").charAt(0) === "#") {
        el.removeAttribute("target");
        el.removeAttribute("rel");
      }
    });
    document.querySelectorAll(".bf-deals").forEach(function (el) { el.remove(); });
  }

  function blackWeekCopy() {
    return {
      es: {
        kicker: "Black Week",
        dates: "23–29 de noviembre",
        text: "Martes 24 o miércoles 25 de noviembre. Solo La Petxina: corte y barba por 20 €. Plazas limitadas.",
        book: "Agenda en Booksy La Petxina",
        flash: "Martes 24 o miércoles 25 · solo La Petxina",
        note: "Los servicios mantienen el precio de la carta. Del 23 al 29 de noviembre, el 10% es solo en productos de tienda, en La Petxina y en El Carmen. El corte y barba por 20 € es el martes 24 o el miércoles 25, solo en La Petxina."
      },
      en: {
        kicker: "Black Week",
        dates: "23–29 November",
        text: "Tuesday 24 or Wednesday 25 November. La Petxina only: haircut and beard for 20 €. Limited slots.",
        book: "Book on Booksy La Petxina",
        flash: "Tue 24 or Wed 25 · La Petxina only",
        note: "Services keep the menu price. From 23 to 29 November, 10% off is only on shop products, at La Petxina and El Carmen. The 20 € haircut and beard is Tuesday 24 or Wednesday 25, at La Petxina only."
      },
      ru: {
        kicker: "Black Week",
        dates: "23–29 ноября",
        text: "Вторник 24 или среда 25 ноября. Только La Petxina: стрижка и борода за 20 €. Мест мало.",
        book: "Запись в Booksy La Petxina",
        flash: "Вт 24 или ср 25 · только La Petxina",
        note: "Услуги остаются по цене прайса. С 23 по 29 ноября скидка 10% только на товары салона, в La Petxina и в El Carmen. Стрижка и борода за 20 € — во вторник 24 или в среду 25, только в La Petxina."
      }
    };
  }

  function isPetxinaFullCut(service) {
    var nameEl = service.querySelector(".service__name");
    if (!nameEl) return false;
    var name = nameEl.textContent.replace(/\s+/g, " ").trim().toLowerCase();
    if (name !== "corte + arreglo de barba" && name !== "cut + beard trim" && name !== "стрижка + борода trim") return false;
    if (/\/la-petxina(?:\.html|\/|$)/i.test(location.pathname)) return true;
    var block = service.closest(".shop-block");
    return !!(block && block.id === "la-petxina");
  }

  function formatCents(cents) {
    var euros = Math.floor(cents / 100);
    var rest = cents % 100;
    if (rest === 0) return euros + " €";
    return euros + "," + (rest < 10 ? "0" : "") + rest + " €";
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
