/* Malerbetrieb Kötter · kleine Helfer für Menü, Vorher-nachher, Galerie, Karte und Formulare */
(function () {
  "use strict";

  /* Menü auf dem Handy */
  var menueKnopf = document.querySelector(".menue-knopf");
  var nav = document.getElementById("hauptmenue");
  if (menueKnopf && nav) {
    menueKnopf.addEventListener("click", function () {
      var offen = nav.classList.toggle("offen");
      menueKnopf.setAttribute("aria-expanded", offen ? "true" : "false");
      menueKnopf.setAttribute("aria-label", offen ? "Menü schließen" : "Menü öffnen");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        nav.classList.remove("offen");
        menueKnopf.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* Vorher-nachher-Regler */
  document.querySelectorAll(".vn").forEach(function (box) {
    var regler = box.querySelector(".vn__regler");
    if (!regler) return;
    var setzen = function () { box.style.setProperty("--pos", regler.value + "%"); };
    regler.addEventListener("input", setzen);
    setzen();
  });

  /* Galerie: Filter und große Ansicht */
  var filter = document.querySelector(".filter");
  if (filter) {
    filter.addEventListener("click", function (e) {
      var knopf = e.target.closest("button");
      if (!knopf) return;
      var wahl = knopf.dataset.filter;
      filter.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", b === knopf ? "true" : "false"); });
      document.querySelectorAll(".galerie li").forEach(function (li) {
        li.hidden = wahl !== "alle" && li.dataset.art !== wahl;
      });
    });
  }
  var lightbox = document.querySelector(".lightbox");
  if (lightbox && typeof lightbox.showModal === "function") {
    var lbBild = lightbox.querySelector("img");
    var lbText = lightbox.querySelector("p");
    document.querySelectorAll(".galerie button").forEach(function (b) {
      b.addEventListener("click", function () {
        var img = b.querySelector("img");
        lbBild.src = b.dataset.gross || img.src;
        lbBild.alt = img.alt;
        lbText.textContent = img.alt;
        lightbox.showModal();
      });
    });
    lightbox.querySelector(".lightbox__zu").addEventListener("click", function () { lightbox.close(); });
    lightbox.addEventListener("click", function (e) { if (e.target === lightbox) lightbox.close(); });
  }

  /* Karte erst nach Klick laden (vorher gehen keine Daten an OpenStreetMap) */
  var karteKnopf = document.querySelector("[data-karte-laden]");
  if (karteKnopf) {
    karteKnopf.addEventListener("click", function () {
      var karte = karteKnopf.closest(".karte");
      var frame = document.createElement("iframe");
      frame.src = karte.dataset.src;
      frame.title = "Karte: Malerbetrieb Kötter, Hauptstraße 41, 49577 Ankum";
      frame.loading = "lazy";
      frame.referrerPolicy = "no-referrer";
      karte.innerHTML = "";
      karte.appendChild(frame);
    });
  }

  /* Formulare: Zeitstempel für den Spamschutz, Versand ohne Seitenwechsel */
  document.querySelectorAll("form[data-formular]").forEach(function (form) {
    var zeit = form.querySelector('input[name="t"]');
    if (zeit) zeit.value = Math.floor(Date.now() / 1000);
    var meldung = form.querySelector(".meldung");
    var knopf = form.querySelector('button[type="submit"]');

    var zeigen = function (ok, text) {
      meldung.hidden = false;
      meldung.className = "meldung " + (ok ? "meldung--ok" : "meldung--fehler");
      meldung.textContent = text;
      meldung.focus();
    };

    form.addEventListener("submit", function (e) {
      if (!window.fetch) return; // ältere Browser: normal abschicken
      e.preventDefault();
      knopf.disabled = true;
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d.ok) {
            form.reset();
            if (zeit) zeit.value = Math.floor(Date.now() / 1000);
            zeigen(true, form.dataset.danke);
          } else {
            zeigen(false, d.meldung || "Das hat leider nicht geklappt. Rufen Sie uns gern an: 05462 00000.");
          }
        })
        .catch(function () { zeigen(false, "Das hat leider nicht geklappt. Rufen Sie uns gern an: 05462 00000."); })
        .then(function () { knopf.disabled = false; });
    });
  });

  /* Rückmeldung, wenn das Formular ohne JavaScript abgeschickt wurde */
  var status = new URLSearchParams(location.search).get("status");
  var form = document.querySelector("form[data-formular]");
  if (status && form) {
    var m = form.querySelector(".meldung");
    m.hidden = false;
    m.className = "meldung " + (status === "ok" ? "meldung--ok" : "meldung--fehler");
    m.textContent = status === "ok" ? form.dataset.danke : "Bitte prüfen Sie Ihre Angaben und versuchen Sie es noch einmal.";
  }

  var jahr = document.getElementById("jahr");
  if (jahr) jahr.textContent = new Date().getFullYear();
})();
