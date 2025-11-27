document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal-ver-tipo');
  const closeButtons = modal?.querySelectorAll('[data-close]');
  const viewButtons = document.querySelectorAll('.btn-view');
  
  function openModal(id) {
    if (!modal) return;
    
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) return;
    
    const nombre = row.getAttribute('data-nombre') || '';
    const descripcion = row.getAttribute('data-descripcion') || '';
    
    const nombreElement = document.getElementById('view-tipo-nombre');
    const descripcionElement = document.getElementById('view-tipo-descripcion');
    
    if (nombreElement) nombreElement.textContent = nombre;
    if (descripcionElement) descripcionElement.textContent = descripcion || '-';
    
    modal.setAttribute('aria-hidden', 'false');
    setTimeout(() => closeButtons?.[0]?.focus(), 100);
  }
  
  function closeModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'true');
  }
  
  // Event listeners para botones ver
  viewButtons.forEach(btn => {
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
