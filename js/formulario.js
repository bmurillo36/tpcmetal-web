/* Validación del formulario en cristiano: dice exactamente qué falta.
   Obligatorio: nombre, un teléfono O un correo, y aceptar la privacidad. */
(function () {
  var formularios = document.querySelectorAll('form.form[novalidate]');

  Array.prototype.forEach.call(formularios, function (form) {
    var aviso   = form.querySelector('.form-error');
    var nombre  = form.querySelector('[name="Nombre"]');
    var tel     = form.querySelector('[name="Telefono"]');
    var email   = form.querySelector('[name="Email"]');
    var acepto  = form.querySelector('[name="Acepto"]');

    function marcar(campo, mal) {
      if (!campo) return;
      var caja = campo.closest('.field') || campo.closest('.consent');
      if (caja) caja.classList.toggle('field--error', !!mal);
      campo.setAttribute('aria-invalid', mal ? 'true' : 'false');
    }

    function revisar() {
      var faltan = [];
      var sinNombre = !nombre.value.trim();
      var sinContacto = !tel.value.trim() && !email.value.trim();
      var emailMal = email.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim());
      var sinAcepto = acepto && !acepto.checked;

      if (sinNombre)   faltan.push('Escriba su <strong>nombre</strong>.');
      if (sinContacto) faltan.push('Deje un <strong>teléfono</strong> para poder llamarle. Si prefiere que le escribamos, ponga su <strong>correo electrónico</strong>.');
      if (emailMal)    faltan.push('Ese <strong>correo electrónico</strong> no parece correcto. Revíselo.');
      if (sinAcepto)   faltan.push('Marque la casilla de <strong>aceptación de la política de privacidad</strong>.');

      marcar(nombre, sinNombre);
      marcar(tel, sinContacto);
      marcar(email, sinContacto || emailMal);
      marcar(acepto, sinAcepto);
      return faltan;
    }

    form.addEventListener('submit', function (e) {
      var faltan = revisar();
      if (!faltan.length) { aviso.hidden = true; return; }
      e.preventDefault();
      aviso.innerHTML =
        '<p class="form-error__titulo">' +
        (faltan.length === 1 ? 'Falta un dato para poder enviar la solicitud'
                             : 'Faltan ' + faltan.length + ' datos para poder enviar la solicitud') +
        '</p><ul>' + faltan.map(function (f) { return '<li>' + f + '</li>'; }).join('') + '</ul>';
      aviso.hidden = false;
      aviso.scrollIntoView({ block: 'center', behavior: 'smooth' });
      var primero = form.querySelector('.field--error input, .field--error textarea, .consent.field--error input');
      if (primero) { try { primero.focus({ preventScroll: true }); } catch (x) { primero.focus(); } }
    });

    // al corregir, quitar el aviso en cuanto quede todo bien
    Array.prototype.forEach.call(form.querySelectorAll('input, textarea, select'), function (c) {
      c.addEventListener('input',  function () { if (!aviso.hidden && !revisar().length) aviso.hidden = true; });
      c.addEventListener('change', function () { if (!aviso.hidden && !revisar().length) aviso.hidden = true; });
    });
  });
})();
