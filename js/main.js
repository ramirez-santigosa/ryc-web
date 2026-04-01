/* ==========================================================================
   INTERACTIVIDAD — Web Convocatoria Ramón y Cajal
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

  // --- Menú móvil (hamburguesa) ---
  const navToggle = document.querySelector('.nav-toggle');
  const navMenu = document.getElementById('nav-menu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function () {
      const isOpen = navMenu.classList.toggle('nav-open');
      navToggle.setAttribute('aria-expanded', isOpen);
      navToggle.innerHTML = isOpen ? '&#10005;' : '&#9776;';
    });

    // Cerrar menú al hacer clic en un enlace (móvil)
    navMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navMenu.classList.remove('nav-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.innerHTML = '&#9776;';
      });
    });
  }

  // --- Acordeones ---
  document.querySelectorAll('.acordeon-header').forEach(function (header) {
    header.addEventListener('click', function () {
      const contenido = this.nextElementSibling;
      const estaActivo = this.classList.contains('activo');

      // Cerrar todos los acordeones del mismo grupo
      this.closest('.seccion').querySelectorAll('.acordeon-header').forEach(function (h) {
        h.classList.remove('activo');
        h.nextElementSibling.classList.remove('activo');
      });

      // Abrir el seleccionado (si no estaba abierto)
      if (!estaActivo) {
        this.classList.add('activo');
        contenido.classList.add('activo');
      }
    });
  });

  // --- Scroll suave para enlaces internos ---
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
