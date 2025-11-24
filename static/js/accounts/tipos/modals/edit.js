document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal-editar-tipo');
  const form = document.getElementById('form-edit-tipo');
  const closeButtons = modal?.querySelectorAll('[data-close]');
  const editButtons = document.querySelectorAll('.btn-edit');
  
  function openModal(id) {
    if (!modal || !form) return;
    
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) return;
    
    form.setAttribute('action', `/accounts/tipos/${id}/editar/`);
    
    const nombre = row.getAttribute('data-nombre') || '';
    const descripcion = row.getAttribute('data-descripcion') || '';
    
    const inputNombre = form.querySelector('[name="nombre"]');
    const inputDescripcion = form.querySelector('[name="descripcion"]');
    
    if (inputNombre) inputNombre.value = nombre;
    if (inputDescripcion) inputDescripcion.value = descripcion;
    
    modal.setAttribute('aria-hidden', 'false');
    setTimeout(() => inputNombre?.focus(), 100);
  }
  
  function closeModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'true');
  }
  
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
