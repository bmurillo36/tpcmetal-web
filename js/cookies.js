/* ===========================================================================
   BANNER DE COOKIES — www.tpcmetal.es
   Centro Médico Siglo XXI, S.L.

   Adaptado del banner de Pedro (Desktop\CLAUDE\banner cookies\banner-cookies.html),
   que sigue la Guía sobre el uso de cookies de la AEPD, el RGPD (UE) 2016/679,
   la LOPDGDD 3/2018 y la LSSI-CE 34/2002.

   Qué se respeta de aquel:
    - Primera capa con tres acciones: Rechazar / Aceptar / Configurar.
    - "Rechazar" tiene el mismo tamaño y peso visual que "Aceptar" (lo exige la AEPD).
    - Las categorías opcionales están DESACTIVADAS por defecto.
    - Nada opcional se ejecuta antes del consentimiento.
    - Enlace permanente para cambiar o revocar la decisión.
    - El consentimiento caduca a los 24 meses.
    - Google Consent Mode v2.

   Qué cambia: aquí el banner se construye desde JavaScript en vez de estar
   escrito en cada página. Son 10 páginas; repetir el HTML en todas ellas es
   pedir que un día se desincronicen. Además evita la avería que tiene
   prevencionderiesgoslaborales.org, donde el banner se coló dentro del <title>
   y así sale en Google.
   =========================================================================== */
(function () {
  "use strict";

  var CLAVE = "tpcmetal_cookies";
  var VERSION = 1;            // súbela si cambian las categorías: vuelve a preguntar
  var MESES = 24;             // máximo que recomienda la AEPD

  /* --- Memoria de la decisión ------------------------------------------- */

  function leer() {
    try {
      var d = JSON.parse(localStorage.getItem(CLAVE));
      if (!d) return null;
      var caducado = (Date.now() - d.ts) > MESES * 30 * 24 * 60 * 60 * 1000;
      if (d.v !== VERSION || caducado) return null;
      return d;
    } catch (e) {
      return null;   // navegación privada, almacenamiento bloqueado, etc.
    }
  }

  function guardar(consent) {
    var dato = { v: VERSION, ts: Date.now(), analisis: !!consent.analisis, preferencias: !!consent.preferencias };
    try { localStorage.setItem(CLAVE, JSON.stringify(dato)); } catch (e) {}
    aplicar(dato);
    ocultarBanner();
    cerrarPanel();
  }

  /* --- Lo que se activa según lo aceptado -------------------------------- */

  function aplicar(c) {
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", {
        analytics_storage:     c.analisis     ? "granted" : "denied",
        functionality_storage: c.preferencias ? "granted" : "denied",
        ad_storage:            "denied",
        ad_user_data:          "denied",
        ad_personalization:    "denied"
      });
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: "consentimiento_cookies",
      cookies_analisis: !!c.analisis,
      cookies_preferencias: !!c.preferencias
    });
  }

  /* --- La ruta a la política, que cambia según la profundidad de la página -- */

  function rutaPolitica() {
    var p = location.pathname.replace(/\/[^\/]*$/, "/");     // carpeta actual
    var hondo = p.split("/").filter(Boolean).length;          // cuántos niveles
    return (hondo ? Array(hondo + 1).join("../") : "") + "pol%C3%ADtica-de-cookies/";
  }

  /* --- Construcción del banner ------------------------------------------ */

  var banner, panel;

  function construir() {
    var pol = rutaPolitica();

    banner = document.createElement("div");
    banner.className = "ck-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-live", "polite");
    banner.setAttribute("aria-label", "Aviso de cookies");
    banner.innerHTML =
      '<div class="ck-banner__inner">' +
        '<div class="ck-banner__texto">' +
          '<p class="ck-titulo">Su privacidad</p>' +
          '<p>Usamos cookies propias y de terceros con fines técnicos, de preferencias y de análisis. ' +
          'Puede aceptarlas todas, rechazarlas o elegir cuáles. Las opcionales no se activan hasta que usted lo consienta. ' +
          'Tiene el detalle en la <a href="' + pol + '">política de cookies</a>.</p>' +
        '</div>' +
        '<div class="ck-banner__acciones">' +
          '<button type="button" class="ck-btn" data-ck="rechazar">Rechazar</button>' +
          '<button type="button" class="ck-btn" data-ck="aceptar">Aceptar</button>' +
          '<button type="button" class="ck-enlace" data-ck="configurar">Configurar</button>' +
        '</div>' +
      '</div>';

    panel = document.createElement("div");
    panel.className = "ck-overlay";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-modal", "true");
    panel.setAttribute("aria-label", "Configuración de cookies");
    panel.innerHTML =
      '<div class="ck-panel">' +
        '<div class="ck-panel__cab">' +
          '<h2>Configuración de cookies</h2>' +
          '<p>Active o desactive cada grupo. Las técnicas son imprescindibles y no se pueden apagar.</p>' +
        '</div>' +
        '<div class="ck-panel__cuerpo">' +
          grupo("Técnicas (necesarias)", "Hacen funcionar la web y no se pueden desactivar. No guardan nada sobre usted.", null, true) +
          grupo("Preferencias", "Recuerdan opciones que usted elige, para no volver a preguntárselas.", "ck-preferencias", false) +
          grupo("Análisis", "Nos dicen, en conjunto y sin identificar a nadie, qué páginas se visitan, para mejorarlas.", "ck-analisis", false) +
        '</div>' +
        '<div class="ck-panel__pie">' +
          '<button type="button" class="ck-btn" data-ck="rechazar">Rechazar todas</button>' +
          '<button type="button" class="ck-btn" data-ck="aceptar">Aceptar todas</button>' +
          '<button type="button" class="ck-btn ck-btn--fuerte" data-ck="guardar">Guardar</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(banner);
    document.body.appendChild(panel);

    document.addEventListener("click", alPulsar);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") cerrarPanel();
    });
  }

  function grupo(titulo, texto, id, fijo) {
    return '<div class="ck-grupo">' +
      '<div><h3>' + titulo + '</h3><p>' + texto + '</p></div>' +
      '<label class="ck-interruptor">' +
        '<input type="checkbox"' + (id ? ' id="' + id + '"' : '') + (fijo ? ' checked disabled' : '') + '>' +
        '<span></span>' +
      '</label>' +
    '</div>';
  }

  /* --- Reacciones -------------------------------------------------------- */

  function alPulsar(e) {
    var b = e.target.closest ? e.target.closest("[data-ck]") : null;
    if (!b) {
      if (e.target === panel) cerrarPanel();
      return;
    }
    var q = b.getAttribute("data-ck");
    if (q === "aceptar")    guardar({ analisis: true,  preferencias: true  });
    if (q === "rechazar")   guardar({ analisis: false, preferencias: false });
    if (q === "configurar") abrirPanel();
    if (q === "guardar")    guardar({
      analisis:     !!(document.getElementById("ck-analisis")     || {}).checked,
      preferencias: !!(document.getElementById("ck-preferencias") || {}).checked
    });
  }

  function abrirPanel() {
    var c = leer();
    var a = document.getElementById("ck-analisis");
    var p = document.getElementById("ck-preferencias");
    if (a) a.checked = c ? !!c.analisis : false;      // por defecto, apagadas
    if (p) p.checked = c ? !!c.preferencias : false;
    panel.classList.add("visible");
  }
  function cerrarPanel()  { if (panel)  panel.classList.remove("visible"); }
  function mostrarBanner(){ if (banner) banner.classList.add("visible"); }
  function ocultarBanner(){ if (banner) banner.classList.remove("visible"); }

  /* --- Arranque ---------------------------------------------------------- */

  function init() {
    construir();
    var c = leer();
    if (c) { aplicar(c); }
    else   { mostrarBanner(); }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
