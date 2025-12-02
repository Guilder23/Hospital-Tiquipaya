document.addEventListener('DOMContentLoaded', function() {
  const mView = document.getElementById('modal-ver-contrato');
  const openModal = (m) => { m.style.display = 'flex'; m.setAttribute('aria-hidden', 'false'); };
  const closeModal = (m) => { m.style.display = 'none'; m.setAttribute('aria-hidden', 'true'); };

  document.querySelectorAll('[data-close]').forEach(el =>
    el.addEventListener('click', () => closeModal(mView))
  );

  document.querySelectorAll('.btn-view').forEach(btn => {
    btn.addEventListener('click', function() {
      const row = document.querySelector(`tr[data-id="${btn.dataset.id}"]`);
      if (!row) return;
      document.getElementById('view-nombre').textContent = row.dataset.nombre || '';
      document.getElementById('view-fecha_inicio').textContent = row.dataset.fecha_inicio || '';
      document.getElementById('view-fecha_fin').textContent = row.dataset.fecha_fin || '';
      document.getElementById('view-estado').textContent = row.dataset.estado === 'true' ? 'Activo' : 'Inactivo';
      openModal(mView);
    });
  });
});

