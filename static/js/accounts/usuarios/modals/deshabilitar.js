document.addEventListener("DOMContentLoaded", function () {

    if (!window.__modals) return;

    const open = window.__modals.open;

    const modalDesactivar = document.getElementById('modal-desactivar-usuario');
    const closeModal = window.__modals.close;

    modalDesactivar.querySelectorAll('[data-close="modal-desactivar-usuario"], [data-close="modal-desactivar"]').forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal(modalDesactivar);
        });
    });

    // 2) Cerrar al hacer click en el overlay (fondo oscuro)
    modalDesactivar.addEventListener('click', e => {
        if (e.target === modalDesactivar) {
            closeModal(modalDesactivar);
        }
    });

    document.querySelectorAll('.btn-toggle').forEach(btn => {
        btn.addEventListener('click', () => {

            const id = btn.dataset.id;
            const username = btn.dataset.username;
            const active = btn.dataset.active.toLowerCase() === "true";

            const modal = document.getElementById('modal-desactivar-usuario');
            const form = document.getElementById('form-desactivar-usuario');
            const texto = document.getElementById('texto-desactivar');
            const titulo = document.getElementById('titulo-modal-usuario');
            const btnSubmit = document.getElementById('btn-submit-modal');

            form.setAttribute('action', `/accounts/usuarios/${id}/toggle/`);

            if (active) {
                titulo.textContent = "Desactivar Usuario";
                texto.textContent = `¿Deseas desactivar a "${username}"?`;
                btnSubmit.textContent = "Desactivar";
            } else {
                titulo.textContent = "Activar Usuario";
                texto.textContent = `¿Deseas activar a "${username}"?`;
                btnSubmit.textContent = "Activar";
            }

            open(modal);
        });
    });

});
