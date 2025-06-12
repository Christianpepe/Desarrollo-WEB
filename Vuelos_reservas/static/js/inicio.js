// JS para el carrusel de Bootstrap y scroll suave en inicio.html

document.addEventListener('DOMContentLoaded', function() {
  // Inicializar el carrusel de Bootstrap si no está activo
  if (window.bootstrap && document.querySelector('.carousel')) {
    var carouselEl = document.querySelector('.carousel');
    var carousel = bootstrap.Carousel.getOrCreateInstance(carouselEl, {
      interval: 5000,
      ride: 'carousel',
      pause: false
    });
  }

  // Scroll suave para los enlaces internos
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href.length > 1 && document.querySelector(href)) {
        e.preventDefault();
        document.querySelector(href).scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });
});
