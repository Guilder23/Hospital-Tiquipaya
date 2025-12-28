document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal-crear-tipo');
  const btnOpen = document.getElementById('btn-open-create');
  const form = document.getElementById('form-create-tipo');
  const closeButtons = modal?.querySelectorAll('[data-close]');
  
  // Elementos para validación
  const nombreInput = document.getElementById('crear-nombre');
  const descripcionInput = document.getElementById('crear-descripcion');
  const nombreCount = document.getElementById('crear-nombre-count');
  const descripcionCount = document.getElementById('crear-descripcion-count');
  const nombreError = document.getElementById('crear-nombre-error');
  const descripcionError = document.getElementById('crear-descripcion-error');
  
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
    
    // Validar nombre
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
    
    // Validar descripción
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
  
  function openModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'false');
    form?.reset();
    
    // Reset contadores y errores
    if (nombreCount) nombreCount.textContent = '0';
    if (descripcionCount) descripcionCount.textContent = '0';
    if (nombreError) nombreError.textContent = '';
    if (descripcionError) descripcionError.textContent = '';
    nombreInput?.classList.remove('input-error');
    descripcionInput?.classList.remove('input-error');
    
    const firstInput = form?.querySelector('input');
    setTimeout(() => firstInput?.focus(), 100);
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
  
  // Abrir modal
  if (btnOpen) {
    btnOpen.addEventListener('click', openModal);
  }
  
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
