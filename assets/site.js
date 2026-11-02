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
    if (link.closest("#reservar, .cta")) return "cta";
    if (link.closest(".service, .service__actions")) return "service";
    if (link.closest(".hero")) return "hero";
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
