document.addEventListener('DOMContentLoaded', function () {
  const asientos = document.querySelectorAll('.asiento');
  const confirmarBtn = document.getElementById('confirmar-btn');
  let asientoSeleccionado = null;

  asientos.forEach(asiento => {
    asiento.addEventListener('click', () => {
      if (asiento.disabled) return;  // Si está reservado, no hace nada

      // Deseleccionar asiento anterior
      if (asientoSeleccionado) {
        asientoSeleccionado.classList.remove('seleccionado');
      }

      // Seleccionar nuevo asiento
      asiento.classList.add('seleccionado');
      asientoSeleccionado = asiento;

      // Habilitar botón de confirmar
      confirmarBtn.disabled = false;
    });
  });

  confirmarBtn.addEventListener('click', () => {
    if (asientoSeleccionado) {
      const asientoNumero = asientoSeleccionado.dataset.asiento;
      confirmarBtn.disabled = true;
      // Asegura que la URL termina en /
      let baseUrl = window.location.pathname;
      if (!baseUrl.endsWith('/')) baseUrl += '/';
      fetch(baseUrl + 'reservar-asiento/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ numero_asiento: asientoNumero })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // Redirigir a página de agradecimiento en la misma pestaña
          const vueloId = window.location.pathname.split('/').filter(Boolean).pop();
          const url = `/vuelos/agradecimiento-reserva/?vuelo_id=${vueloId}&asiento=${encodeURIComponent(asientoNumero)}`;
          window.location.href = url;
        } else {
          alert(data.error || 'Error al reservar asiento');
          confirmarBtn.disabled = false;
        }
      })
      .catch(() => {
        alert('Error de red o sesión expirada. Inicia sesión nuevamente.');
        confirmarBtn.disabled = false;
      });
    }
  });

  // Utilidad para CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
