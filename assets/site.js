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
