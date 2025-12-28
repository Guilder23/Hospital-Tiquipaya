document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal-editar-tipo');
  const form = document.getElementById('form-edit-tipo');
  const closeButtons = modal?.querySelectorAll('[data-close]');
  const editButtons = document.querySelectorAll('.btn-edit');
  
  // Elementos para validación
  const nombreInput = document.getElementById('editar-nombre');
  const descripcionInput = document.getElementById('editar-descripcion');
  const nombreCount = document.getElementById('editar-nombre-count');
  const descripcionCount = document.getElementById('editar-descripcion-count');
  const nombreError = document.getElementById('editar-nombre-error');
  const descripcionError = document.getElementById('editar-descripcion-error');
  
  function updateCharCount(input, countElement, maxLength) {
    if (!input || !countElement) return;
    const length = input.value.length;
    countElement.textContent = length;
    
    if (length >= maxLength) {
      countElement.parentElement.classList.add('limit-reached');
    } else {
      countElement.parentElement.classList.remove('limit-reached');
    }
  }
  
  function validateForm() {
    let isValid = true;
    
    if (nombreInput) {
      const nombre = nombreInput.value.trim();
      if (nombre.length === 0) {
        nombreError.textContent = 'El nombre es obligatorio';
        nombreInput.classList.add('input-error');
        isValid = false;
      } else if (nombre.length > 50) {
        nombreError.textContent = 'El nombre no puede exceder 50 caracteres';
        nombreInput.classList.add('input-error');
        isValid = false;
      } else {
        nombreError.textContent = '';
        nombreInput.classList.remove('input-error');
      }
    }
    
    if (descripcionInput) {
      const desc = descripcionInput.value;
      if (desc.length > 200) {
        descripcionError.textContent = 'La descripción no puede exceder 200 caracteres';
        descripcionInput.classList.add('input-error');
        isValid = false;
      } else {
        descripcionError.textContent = '';
        descripcionInput.classList.remove('input-error');
      }
    }
    
    return isValid;
  }
  
  function openModal(id) {
    if (!modal || !form) return;
    
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) return;
    
    form.setAttribute('action', `/accounts/tipos/${id}/editar/`);
    
    const nombre = row.getAttribute('data-nombre') || '';
    const descripcion = row.getAttribute('data-descripcion') || '';
    
    if (nombreInput) {
      nombreInput.value = nombre;
      updateCharCount(nombreInput, nombreCount, 50);
    }
    if (descripcionInput) {
      descripcionInput.value = descripcion;
      updateCharCount(descripcionInput, descripcionCount, 200);
    }
    
    // Limpiar errores
    if (nombreError) nombreError.textContent = '';
    if (descripcionError) descripcionError.textContent = '';
    nombreInput?.classList.remove('input-error');
    descripcionInput?.classList.remove('input-error');
    
    modal.setAttribute('aria-hidden', 'false');
    setTimeout(() => nombreInput?.focus(), 100);
  }
  
  function closeModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'true');
  }
  
  // Validación en tiempo real para solo permitir letras
  nombreInput?.addEventListener('input', function(e) {
    // Permitir solo letras (incluyendo acentos y ñ), espacios
    const regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g;
    if (regex.test(this.value)) {
      this.value = this.value.replace(regex, '');
    }
    updateCharCount(nombreInput, nombreCount, 50);
  });
  
  // Event listeners para contadores
  descripcionInput?.addEventListener('input', () => updateCharCount(descripcionInput, descripcionCount, 200));
  
  // Validación al enviar
  form?.addEventListener('submit', function(e) {
    if (!validateForm()) {
      e.preventDefault();
    }
  });
  
  // Event listeners para botones editar
  editButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const id = this.getAttribute('data-id');
      openModal(id);
    });
  });
  
  // Cerrar modal
  closeButtons?.forEach(btn => {
    btn.addEventListener('click', closeModal);
  });
  
  // Cerrar al presionar ESC
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal?.getAttribute('aria-hidden') === 'false') {
      closeModal();
    }
  });
  
  // Cerrar al hacer click en el backdrop
  const backdrop = modal?.querySelector('.modal-backdrop');
  backdrop?.addEventListener('click', closeModal);
});
