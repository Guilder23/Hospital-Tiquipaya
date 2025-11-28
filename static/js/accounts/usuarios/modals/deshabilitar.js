document.addEventListener("DOMContentLoaded", function () {
    if (!window.__modals) return;

    const { open, close } = window.__modals;

    const modalDesactivar = document.getElementById('modal-desactivar-usuario');
    const form = document.getElementById('form-desactivar-usuario');

    if (!modalDesactivar || !form) return;

    // ---------------- CERRAR MODAL ----------------
    modalDesactivar.querySelectorAll('[data-close="modal-desactivar-usuario"], [data-close="modal-desactivar"]')
        .forEach(btn => btn.addEventListener('click', () => close(modalDesactivar)));

    modalDesactivar.addEventListener('click', e => {
        if (e.target === modalDesactivar) close(modalDesactivar);
    });

    // ---------------- BOTONES DE TOGGLE ----------------
    document.querySelectorAll('.btn-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const username = btn.dataset.username || '';
            const activeRaw = (btn.dataset.active || '').toLowerCase();
            const active = activeRaw === "true" || activeRaw === "1";

            if (!id) return console.warn('btn-toggle sin data-id');

            // Actualizar modal
            modalDesactivar.querySelector('#titulo-modal-usuario').textContent = active ? "Desactivar Usuario" : "Activar Usuario";
            modalDesactivar.querySelector('#texto-desactivar').textContent = active
                ? `¿Deseas desactivar a "${username}"?`
                : `¿Deseas activar a "${username}"?`;

            const btnSubmit = modalDesactivar.querySelector('#btn-submit-modal');
            btnSubmit.textContent = active ? "Desactivar" : "Activar";
            btnSubmit.classList.toggle('btn-danger', active);
            btnSubmit.classList.toggle('btn-success', !active);

            // Configurar action del form
            form.action = `/accounts/usuarios/${id}/toggle/`;

            // Abrir modal
            open(modalDesactivar);
        });
    });

    // ---------------- ENVIAR FORMULARIO ----------------
    form.addEventListener('submit', e => {
        // No previenes submit, se envía normalmente al servidor
        close(modalDesactivar); // opcional: cerrar modal al enviar
    });
});
