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
      const data = {
        nombre: formCreate['nombre'].value,
        fecha_inicio: formCreate['fecha_inicio'].value,
        fecha_fin: formCreate['fecha_fin'].value,
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
      }
    });
  }
});

