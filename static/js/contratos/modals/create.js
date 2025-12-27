document.addEventListener('DOMContentLoaded', function() {
  const mCreate = document.getElementById('modal-crear-contrato');
  const formCreate = document.getElementById('form-create-contrato');
  const btnOpenCreate = document.getElementById('btn-open-create');
  const apiUrl = '/contratos/api/';

  const openModal = (m) => { if (m) { m.style.display = 'flex'; m.setAttribute('aria-hidden', 'false'); } };
  const closeModal = (m) => { if (m) { m.style.display = 'none'; m.setAttribute('aria-hidden', 'true'); } };
  const getCsrfToken = () => document.querySelector('[name=csrfmiddlewaretoken]').value;

  if (btnOpenCreate) {
    btnOpenCreate.addEventListener('click', () => {
      if (formCreate) formCreate.reset();
      openModal(mCreate);
    });
  }

  document.querySelectorAll('[data-close]').forEach(el =>
    el.addEventListener('click', () => closeModal(mCreate))
  );

  if (formCreate) {
    formCreate.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const errorDiv = document.getElementById('create-error-message');
      errorDiv.style.display = 'none';
      errorDiv.textContent = '';
      
      const fechaInicio = formCreate['fecha_inicio'].value;
      const fechaFin = formCreate['fecha_fin'].value;
      
      // Validación: fecha inicio no puede ser mayor que fecha fin (pueden ser iguales)
      if (fechaInicio > fechaFin) {
        errorDiv.textContent = 'La fecha de inicio no puede ser mayor que la fecha de fin';
        errorDiv.style.display = 'block';
        return;
      }
      
      const data = {
        nombre: formCreate['nombre'].value,
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
      };

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        closeModal(mCreate);
        window.location.reload();
      } else {
        const errorData = await response.json();
        errorDiv.textContent = 'Error al crear el contrato: ' + (errorData.error || 'Error desconocido');
        errorDiv.style.display = 'block';
      }
    });
  }
});

