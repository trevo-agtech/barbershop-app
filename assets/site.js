(function () {
  function channelOf(href) {
    if (/agenda\.barbershopvalencia\.es/i.test(href)) return "agenda";
    if (/booksy\.com/i.test(href)) return "booksy";
    if (/whatsapp\.com|wa\.me/i.test(href)) return "whatsapp";
    if (/instagram\.com/i.test(href)) return "instagram";
    if (/facebook\.com|fb\.com/i.test(href)) return "facebook";
    if (/tiktok\.com/i.test(href)) return "tiktok";
    if (/google\.com\/maps|maps\.google|goo\.gl\/maps/i.test(href)) return "maps";
    if (/^mailto:/i.test(href)) return "email";
    if (/^tel:/i.test(href)) return "phone";
    return "";
  }

  function isBookingChannel(channel) {
    return channel === "agenda" || channel === "booksy" || channel === "whatsapp";
  }

  function isReserveCta(href, label) {
    if (/^#(reservar|tiendas)\b/i.test(href)) return true;
    if (/agenda\.barbershopvalencia\.es|booksy\.com/i.test(href)) return true;
    if (/whatsapp\.com|wa\.me/i.test(href) && /reserv|agendar|book|запис|whatsapp/i.test(label)) return true;
    return /reserv|agendar|\bbook\b|запис/i.test(label);
  }

  function shopFrom(href, label, pathname) {
    var page = pathname != null ? pathname : location.pathname;
    var clean = String(href || "").replace(/[?&](?:utm_[a-z]+|utc)=[^&#]*/gi, "");
    var hay = (clean + " " + label).toLowerCase();
    var carmen = /local=el-carmen|local=carmen\b|el[- ]carmen|132769|34634456940/.test(hay);
    var petxinaLink = /local=la-petxina|local=petxina\b|petxina|12979/.test(hay);
    var defaultWhatsapp = /34677142958/.test(hay) && !petxinaLink;
    if (carmen && !petxinaLink) return "el_carmen";
    if (petxinaLink && !carmen) return "la_petxina";
    if (defaultWhatsapp) {
      if (/\/la-petxina(?:\.html|\/|$)/i.test(page)) return "la_petxina";
      if (/\/el-carmen(?:\.html|\/|$)/i.test(page)) return "el_carmen";
      return "general";
    }
    if (/juan(?:\s|\+|%20)*llorens/.test(hay)) return "la_petxina";
    if (/google\.com\/maps|maps\.google/.test(hay) && /baja/.test(hay)) return "el_carmen";
    if (/\/el-carmen(?:\.html|\/|$)/i.test(page)) return "el_carmen";
    if (/\/la-petxina(?:\.html|\/|$)/i.test(page)) return "la_petxina";
    return "general";
  }

  function bookingTags(href, label, pathname, blackFriday) {
    var channel = channelOf(href);
    var shop = shopFrom(href, label, pathname);
    return {
      channel: channel,
      shop: shop,
      medium: isBookingChannel(channel) ? channel : "",
      campaign: blackFriday ? "black_friday" : (isBookingChannel(channel) ? "reservar" : (channel || "reservar")),
      reserve: isReserveCta(href, label)
    };
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { channelOf: channelOf, shopFrom: shopFrom, isReserveCta: isReserveCta, isBookingChannel: isBookingChannel, bookingTags: bookingTags };
  }

  if (typeof document === "undefined") return;

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
      trackEvent("menu_toggle", {
        menu_state: open ? "open" : "close",
        page_path: location.pathname,
        language: languageCode(),
        placement: "header"
      });
    });
  }

  document.querySelectorAll("[data-drop-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      if (window.matchMedia("(max-width: 899px)").matches) {
        event.preventDefault();
        var item = btn.closest(".nav__drop");
        var open = item.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
        trackEvent("nav_dropdown", {
          menu_state: open ? "open" : "close",
          link_text: linkLabel(btn),
          page_path: location.pathname,
          language: languageCode(),
          placement: "header"
        });
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
      if (lightbox.hidden) return;
      lightbox.hidden = true;
      document.body.classList.remove("is-locked");
      trackEvent("gallery_close", {
        page_path: location.pathname,
        language: languageCode(),
        placement: "gallery"
      });
    };
    document.querySelectorAll("[data-gallery] img").forEach(function (photo) {
      photo.addEventListener("click", function () {
        img.src = photo.currentSrc || photo.src;
        img.alt = photo.alt;
        if (caption) caption.textContent = photo.alt;
        lightbox.hidden = false;
        document.body.classList.add("is-locked");
        trackEvent("gallery_open", {
          link_text: photo.alt || "",
          page_path: location.pathname,
          language: languageCode(),
          placement: "gallery"
        });
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
    var formStarted = false;
    form.addEventListener("focusin", function () {
      if (formStarted) return;
      formStarted = true;
      trackEvent("form_start", {
        form_type: "contacto",
        page_path: location.pathname,
        language: languageCode(),
        placement: "contact"
      });
    });
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
      window.location.href = "mailto:infobarbershopvalencia@gmail.com?subject=" + subject + "&body=" + body;
      var note = form.querySelector("[data-form-note]");
      if (note) {
        note.hidden = false;
        note.textContent = "Se abrió tu correo para enviar el mensaje a infobarbershopvalencia@gmail.com.";
      }
    });
  }

  mountBlackWeek();
  mountChristmas();
  stampOutboundLinks();

  document.addEventListener("click", function (event) {
    var link = event.target.closest("a");
    if (!link) return;
    stampLink(link);
    var href = link.getAttribute("href") || "";
    if (!href || href === "#" || /^javascript:/i.test(href)) return;
    var label = linkLabel(link);
    var channel = link.dataset.gaChannel || channelOf(href);
    var reservar = isReserveCta(href, label);
    if (!channel && !reservar) {
      trackInternalClick(link, href, label);
      return;
    }
    if (href.charAt(0) === "#" && !/^#(reservar|tiendas)\b/i.test(href)) {
      trackInternalClick(link, href, label);
      return;
    }

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
    if (channel === "agenda") {
      trackEvent("click_agenda", params);
      if (params.shop === "el_carmen") trackEvent("click_agenda_el_carmen", params);
      if (params.shop === "la_petxina") trackEvent("click_agenda_la_petxina", params);
    }
    if (channel === "instagram") trackEvent("click_instagram", params);
    if (channel === "facebook") trackEvent("click_facebook", params);
    if (channel === "tiktok") trackEvent("click_tiktok", params);
    if (channel === "maps") trackEvent("click_maps", params);
    if (channel === "email") trackEvent("click_email", params);
    if (channel === "phone") trackEvent("click_phone", params);
    if (params.utm_campaign === "black_friday") {
      trackEvent("click_black_friday", params);
      if (params.shop === "el_carmen") trackEvent("click_black_friday_el_carmen", params);
      if (params.shop === "la_petxina") trackEvent("click_black_friday_la_petxina", params);
    }
    if (reservar) {
      params.channel = channel || "page";
      trackEvent("click_reservar", params);
    }
    if (isBookingChannel(channel)) {
      trackEvent("booking_click", {
        booking_method: channel,
        shop: params.shop,
        placement: params.placement,
        language: params.language,
        page_path: params.page_path,
        link_url: href
      });
    }
  });

  function trackInternalClick(link, href, label) {
    var params = trackingParams(link, href, label, "page");
    trackEvent("click_internal", params);
    if (link.closest(".lang")) {
      trackEvent("click_language", {
        link_text: label,
        language_to: (link.getAttribute("hreflang") || "").slice(0, 2),
        page_path: location.pathname,
        language: languageCode(),
        placement: "language"
      });
    }
    if (/\/blog\//i.test(href) || (/\/blog\//i.test(location.pathname) && /^\.\//.test(href))) trackEvent("click_blog", params);
    if (/el-carmen\.html/i.test(href)) trackEvent("click_shop_el_carmen", params);
    if (/la-petxina\.html/i.test(href)) trackEvent("click_shop_la_petxina", params);
    if (/servicios\.html|services\.html/i.test(href)) trackEvent("click_services", params);
    if (/contacto\.html|contact\.html/i.test(href)) trackEvent("click_contact", params);
    if (/^#horario\b/i.test(href)) trackEvent("click_hours", params);
  }

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
    var campaign = campaignOf(link, channel);
    var utc = utcCode(link, href, channel);
    var booking = isBookingChannel(channel);
    if (!link.dataset.gaChannel) link.dataset.gaChannel = channel;
    try {
      var url = new URL(href, location.href);
      if (!url.searchParams.has("utm_source")) {
        url.searchParams.set("utm_source", "website");
        url.searchParams.set("utm_medium", booking ? channel : placement);
        url.searchParams.set("utm_campaign", campaign);
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
      utm_medium: isBookingChannel(channel) ? channel : placementOf(link),
      utm_campaign: campaignOf(link, channel),
      utm_content: shopFrom(href, label),
      utm_term: pageCode(),
      utc: link.dataset.utc || utcCode(link, href, channel || "reservar"),
      bf_offer: blackFridayOffer(link)
    };
  }

  function isBlackFridayLink(link) {
    return !!(link.closest(".bf-bar, .bf-deals, [data-bf-link]") || link.hasAttribute("data-bf-restore-href"));
  }

  function campaignOf(link, channel) {
    if (isBlackFridayLink(link)) return "black_friday";
    if (isBookingChannel(channel)) return "reservar";
    return channel || "reservar";
  }

  function blackFridayOffer(link) {
    if (!isBlackFridayLink(link)) return "";
    if (link.closest(".bf-modal")) return "modal";
    if (link.closest(".bf-bar")) return "bar";
    if (link.closest(".bf-deal--flash")) return "corte_20";
    if (link.closest(".bf-deals")) return "productos_10";
    if (link.closest(".hero")) return "hero";
    return "articulo";
  }

  function utcCode(link, href, channel) {
    var parts = [channel, shopFrom(href, linkLabel(link)), placementOf(link), languageCode()];
    if (isBlackFridayLink(link)) parts.unshift("black_friday");
    return parts.join("_");
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

  function placementOf(link) {
    if (link.classList.contains("wa")) return "floating";
    if (link.closest(".xmas-bar")) return "banner";
    if (link.closest(".lang")) return "language";
    if (link.closest(".blog-card, .blog-post")) return "blog";
    if (link.closest(".nav, header")) return "header";
    if (link.closest("footer, .footer")) return "footer";
    if (link.closest(".bf-modal")) return "modal";
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
    var petxina = "https://agenda.barbershopvalencia.es/?local=la-petxina";
    var booksyPetxina = "https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia";
    var whatsappPetxina = "https://api.whatsapp.com/send/?phone=34677142958&text=" + encodeURIComponent(t.whatsappText) + "&type=phone_number&app_absent=0";
    var bar = document.createElement("div");
    bar.className = "bf-bar";
    bar.innerHTML =
      '<div class="bf-bar__inner container">' +
        '<p class="bf-bar__copy"><strong>' + t.kicker + '</strong>' +
        '<span class="bf-bar__dates">' + t.dates + '</span>' +
        '<span>' + t.text + '</span></p>' +
        '<div class="bf-bar__actions">' +
          '<a class="btn btn--primary btn--sm" href="' + petxina + '" data-ga-channel="agenda">' + t.book + '</a>' +
          '<a class="btn btn--ghost btn--sm" href="' + booksyPetxina + '" target="_blank" rel="noopener" data-ga-channel="booksy">' + t.booksy + '</a>' +
          '<a class="btn btn--ghost btn--sm" href="' + whatsappPetxina + '" target="_blank" rel="noopener" data-ga-channel="whatsapp">' + t.whatsapp + '</a>' +
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
    mountBlackFridayModal(t, petxina);
  }

  function mountBlackFridayModal(t, petxina) {
    if (!window.matchMedia("(min-width: 960px)").matches) return;
    try {
      if (sessionStorage.getItem("bf-modal") === "1") return;
    } catch (error) {}
    var carmen = "https://agenda.barbershopvalencia.es/?local=el-carmen";
    var booksyPetxina = "https://booksy.com/es-es/12979_barber-shop-valencia_barberia_58087_valencia";
    var whatsappPetxina = "https://api.whatsapp.com/send/?phone=34677142958&text=" + encodeURIComponent(t.whatsappText) + "&type=phone_number&app_absent=0";
    var modal = document.createElement("div");
    modal.className = "bf-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "bf-modal-title");
    modal.setAttribute("data-bf-link", "");
    modal.innerHTML =
      '<div class="bf-modal__backdrop" data-bf-close></div>' +
      '<div class="bf-modal__panel">' +
        '<button type="button" class="bf-modal__close" data-bf-close aria-label="' + t.close + '">×</button>' +
        '<p class="bf-modal__kicker">' + t.kicker + '</p>' +
        '<p class="bf-modal__price">20 €</p>' +
        '<h2 id="bf-modal-title">' + t.modalTitle + '</h2>' +
        '<p class="bf-modal__when">' + t.modalWhen + '</p>' +
        '<p class="bf-modal__detail">' + t.modalDetail + '</p>' +
        '<div class="bf-modal__side"><strong>10%</strong><span>' + t.modalProducts + '</span></div>' +
        '<div class="bf-modal__actions">' +
          '<a class="btn btn--primary" href="' + petxina + '" data-ga-channel="agenda">' + t.book + '</a>' +
          '<a class="btn btn--ghost" href="' + booksyPetxina + '" target="_blank" rel="noopener" data-ga-channel="booksy">' + t.booksy + '</a>' +
          '<a class="btn btn--ghost" href="' + whatsappPetxina + '" target="_blank" rel="noopener" data-ga-channel="whatsapp">' + t.whatsapp + '</a>' +
          '<a class="btn btn--ghost" href="' + carmen + '" data-ga-channel="agenda">' + t.bookCarmen + '</a>' +
        '</div>' +
      '</div>';
    document.body.appendChild(modal);
    document.body.classList.add("bf-modal-open");
    var closeBtn = modal.querySelector(".bf-modal__close");
    if (closeBtn) closeBtn.focus();
    function close() {
      if (!modal.isConnected) return;
      modal.remove();
      document.body.classList.remove("bf-modal-open");
      try { sessionStorage.setItem("bf-modal", "1"); } catch (error) {}
    }
    modal.querySelectorAll("[data-bf-close]").forEach(function (el) {
      el.addEventListener("click", close);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") close();
    });
  }

  function blackWeekOpen() {
    return false;
  }

  function mountChristmas() {
    if (!christmasOpen()) return;
    document.body.classList.add("is-christmas");
    var lang = languageCode();
    var copy = christmasCopy();
    var t = copy[lang] || copy.es;
    var bar = document.createElement("div");
    bar.className = "xmas-bar";
    bar.innerHTML =
      '<div class="xmas-bar__inner container">' +
        '<p class="xmas-bar__copy"><strong>' + t.kicker + '</strong><a href="' + christmasPostHref() + '">' + t.text + '</a></p>' +
      '</div>';
    document.body.insertBefore(bar, document.body.firstChild);
    function fitBar() {
      document.body.style.setProperty("--xmas-h", bar.offsetHeight + "px");
    }
    fitBar();
    window.addEventListener("resize", fitBar);
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var snow = document.createElement("div");
    snow.className = "snow";
    snow.setAttribute("aria-hidden", "true");
    var flakes = ["❄", "❅", "❆"];
    var html = "";
    for (var i = 0; i < 42; i++) {
      var size = (7 + Math.random() * 11).toFixed(1);
      var left = (Math.random() * 100).toFixed(2);
      var duration = (10 + Math.random() * 14).toFixed(2);
      var delay = (-Math.random() * 18).toFixed(2);
      var drift = ((Math.random() * 70) - 35).toFixed(0);
      var opacity = (0.55 + Math.random() * 0.4).toFixed(2);
      html += '<i style="left:' + left + '%;font-size:' + size + 'px;animation-duration:' + duration + 's;animation-delay:' + delay + 's;opacity:' + opacity + ';--snow-x:' + drift + 'px">' + flakes[i % 3] + '</i>';
    }
    snow.innerHTML = html;
    document.body.appendChild(snow);
  }

  function christmasPostHref() {
    var lang = languageCode();
    var file = lang === "en"
      ? "christmas-sunday-la-petxina-open.html"
      : lang === "ru"
        ? "rozhdestvenskoe-voskresene-la-petxina-otkryta.html"
        : "domingo-navidad-la-petxina-abierta.html";
    if (/\/blog\//i.test(location.pathname)) return "./" + file;
    return "./blog/" + file;
  }

  function christmasOpen() {
    var day;
    try {
      day = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Madrid", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
    } catch (error) {
      day = new Date().toISOString().slice(0, 10);
    }
    return day >= "2026-11-26" && day <= "2027-01-06";
  }

  function christmasCopy() {
    return {
      es: {
        kicker: "Navidad",
        text: "En diciembre, solo La Petxina abre los domingos de 10:00 a 14:00. Domingo de Navidad: 27 de diciembre."
      },
      en: {
        kicker: "Christmas",
        text: "In December, only La Petxina is open on Sundays, 10:00–14:00. Christmas Sunday: 27 December."
      },
      ru: {
        kicker: "Рождество",
        text: "В декабре по воскресеньям открыта только La Petxina, с 10:00 до 14:00. Рождественское воскресенье: 27 декабря."
      }
    };
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
        book: "Agendar La Petxina",
        booksy: "Booksy",
        whatsapp: "WhatsApp",
        whatsappText: "Hola, quiero reservar en Barber Shop Valencia La Petxina.",
        bookCarmen: "Agendar El Carmen",
        close: "Cerrar",
        modalTitle: "Corte y barba, un solo día",
        modalWhen: "Martes 24 o miércoles 25 de noviembre",
        modalDetail: "Solo en La Petxina, Juan Llorens 18. Elige un día. Plazas limitadas.",
        modalProducts: "Del 23 al 29 de noviembre, solo en productos de tienda. La Petxina y El Carmen.",
        flash: "Martes 24 o miércoles 25 · solo La Petxina",
        note: "Los servicios mantienen el precio de la carta. Del 23 al 29 de noviembre, el 10% es solo en productos de tienda, en La Petxina y en El Carmen. El corte y barba por 20 € es el martes 24 o el miércoles 25, solo en La Petxina."
      },
      en: {
        kicker: "Black Week",
        dates: "23–29 November",
        text: "Tuesday 24 or Wednesday 25 November. La Petxina only: haircut and beard for 20 €. Limited slots.",
        book: "Book La Petxina",
        booksy: "Booksy",
        whatsapp: "WhatsApp",
        whatsappText: "Hi, I want to book at Barber Shop Valencia La Petxina.",
        bookCarmen: "Book El Carmen",
        close: "Close",
        modalTitle: "Haircut and beard, one day",
        modalWhen: "Tuesday 24 or Wednesday 25 November",
        modalDetail: "La Petxina only, Juan Llorens 18. Pick one day. Limited slots.",
        modalProducts: "23–29 November, shop products only. La Petxina and El Carmen.",
        flash: "Tue 24 or Wed 25 · La Petxina only",
        note: "Services keep the menu price. From 23 to 29 November, 10% off is only on shop products, at La Petxina and El Carmen. The 20 € haircut and beard is Tuesday 24 or Wednesday 25, at La Petxina only."
      },
      ru: {
        kicker: "Black Week",
        dates: "23–29 ноября",
        text: "Вторник 24 или среда 25 ноября. Только La Petxina: стрижка и борода за 20 €. Мест мало.",
        book: "Запись La Petxina",
        booksy: "Booksy",
        whatsapp: "WhatsApp",
        whatsappText: "Здравствуйте, хочу записаться в Barber Shop Valencia La Petxina.",
        bookCarmen: "Запись El Carmen",
        close: "Закрыть",
        modalTitle: "Стрижка и борода, один день",
        modalWhen: "Вторник 24 или среда 25 ноября",
        modalDetail: "Только La Petxina, Juan Llorens 18. Выберите один день. Мест мало.",
        modalProducts: "С 23 по 29 ноября, только товары салона. La Petxina и El Carmen.",
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
