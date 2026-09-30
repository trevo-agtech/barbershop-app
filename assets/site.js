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
      window.location.href = "mailto:info@barbershopvalencia.com?subject=" + subject + "&body=" + body;
      var note = form.querySelector("[data-form-note]");
      if (note) {
        note.hidden = false;
        note.textContent = "Se abrió tu correo para enviar el mensaje a info@barbershopvalencia.com.";
      }
    });
  }
})();
