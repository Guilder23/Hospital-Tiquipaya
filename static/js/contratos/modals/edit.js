document.addEventListener('DOMContentLoaded', function() {
  const mEdit = document.getElementById('modal-editar-contrato');
  const formEdit = document.getElementById('form-edit-contrato');
  const apiUrl = '/contratos/api/';

  const openModal = (m) => { m.setAttribute('aria-hidden', 'false'); m.style.display = 'flex'; };
  const closeModal = (m) => { m.setAttribute('aria-hidden', 'true'); m.style.display = 'none'; };
  const getCsrfToken = () => document.querySelector('[name=csrfmiddlewaretoken]').value;

  document.querySelectorAll('[data-close]').forEach(el =>
    el.addEventListener('click', () => closeModal(mEdit))
  );

  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', function() {
      const id = btn.dataset.id;
      const nombre = btn.dataset.nombre;
      const fechaInicio = btn.dataset.fecha_inicio;
      const fechaFin = btn.dataset.fecha_fin;
      const estado = btn.dataset.estado;

      document.getElementById('edit-id').value = id;
      document.getElementById('edit-nombre').value = nombre;
      document.getElementById('edit-fecha_inicio').value = fechaInicio;
      document.getElementById('edit-fecha_fin').value = fechaFin;
      document.getElementById('edit-estado').value = estado === "true" ? "true" : "false";

      openModal(mEdit);
    });
  });

  if (formEdit) {
    formEdit.addEventListener('submit', async function(e) {
      e.preventDefault();
      const id = document.getElementById('edit-id').value;
      const data = {
        nombre: formEdit['nombre'].value,
        fecha_inicio: formEdit['fecha_inicio'].value,
        fecha_fin: formEdit['fecha_fin'].value,
        estado: formEdit['estado'].value === 'true'
      };

      const response = await fetch(`${apiUrl}${id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        closeModal(mEdit);
        window.location.reload();
      }
    });
  }
});

