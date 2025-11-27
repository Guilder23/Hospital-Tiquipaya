document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal-eliminar-tipo');
  const form = document.getElementById('form-delete-tipo');
  const closeButtons = modal?.querySelectorAll('[data-close]');
  const deleteButtons = document.querySelectorAll('.btn-delete');
  
  function openModal(id, nombre) {
    if (!modal || !form) return;
    
    form.setAttribute('action', `/accounts/tipos/${id}/eliminar/`);
    
    const textElement = document.getElementById('delete-tipo-text');
    if (textElement) {
      textElement.textContent = `¿Confirmas eliminar "${nombre}"?`;
    }
    
    modal.setAttribute('aria-hidden', 'false');
    setTimeout(() => form.querySelector('.btn-danger')?.focus(), 100);
  }
  
  function closeModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'true');
  }
  
  // Event listeners para botones eliminar
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const id = this.getAttribute('data-id');
      const nombre = this.getAttribute('data-nombre');
      openModal(id, nombre);
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
