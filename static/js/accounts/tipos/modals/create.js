document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal-crear-tipo');
  const btnOpen = document.getElementById('btn-open-create');
  const form = document.getElementById('form-create-tipo');
  const closeButtons = modal?.querySelectorAll('[data-close]');
  
  function openModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'false');
    form?.reset();
    // Focus en el primer input
    const firstInput = form?.querySelector('input');
    setTimeout(() => firstInput?.focus(), 100);
  }
  
  function closeModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'true');
  }
  
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
