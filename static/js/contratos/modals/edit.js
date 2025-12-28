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

  // ========== VALIDACIONES EN TIEMPO REAL ==========
  // Validar nombre: solo caracteres alfabéticos
  const nombreInput = document.getElementById('edit-nombre');
  if(nombreInput){
    nombreInput.addEventListener('input', function() {
      const regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g;
      if (regex.test(this.value)) {
        this.value = this.value.replace(regex, '');
      }
    });
  }

  // Validar fechas: fecha fin debe ser al menos 1 día después de fecha inicio
  const fechaInicioInput = document.getElementById('edit-fecha_inicio');
  const fechaFinInput = document.getElementById('edit-fecha_fin');
  
  function validarFechasContratoEdit() {
    if(fechaInicioInput && fechaFinInput) {
      // Si hay fecha inicio, la fecha fin debe ser al menos 1 día después
      if(fechaInicioInput.value) {
        const fechaInicio = new Date(fechaInicioInput.value);
        fechaInicio.setDate(fechaInicio.getDate() + 1);
        const minFechaFin = fechaInicio.toISOString().split('T')[0];
        fechaFinInput.setAttribute('min', minFechaFin);
      }
      // Si hay fecha fin, la fecha inicio no puede ser mayor o igual
      if(fechaFinInput.value) {
        const fechaFin = new Date(fechaFinInput.value);
        fechaFin.setDate(fechaFin.getDate() - 1);
        const maxFechaInicio = fechaFin.toISOString().split('T')[0];
        fechaInicioInput.setAttribute('max', maxFechaInicio);
      }
    }
  }
  
  if(fechaInicioInput) fechaInicioInput.addEventListener('change', validarFechasContratoEdit);
  if(fechaFinInput) fechaFinInput.addEventListener('change', validarFechasContratoEdit);

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
      document.getElementById('edit-estado').value = (estado === 'true') ? 'true' : 'false';

      openModal(mEdit);
    });
  });

  if (formEdit) {
    formEdit.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const errorDiv = document.getElementById('edit-error-message');
      errorDiv.style.display = 'none';
      errorDiv.textContent = '';
      
      const id = document.getElementById('edit-id').value;
      const fechaInicio = formEdit['fecha_inicio'].value;
      const fechaFin = formEdit['fecha_fin'].value;
      
      // Validación: fecha inicio no puede ser mayor que fecha fin (pueden ser iguales)
      if (fechaInicio > fechaFin) {
        errorDiv.textContent = 'La fecha de inicio no puede ser mayor que la fecha de fin';
        errorDiv.style.display = 'block';
        return;
      }
      
      const data = {
        nombre: formEdit['nombre'].value,
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
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
      } else {
        const errorData = await response.json();
        errorDiv.textContent = 'Error al actualizar el contrato: ' + (errorData.error || 'Error desconocido');
        errorDiv.style.display = 'block';
      }
    });
  }
});
