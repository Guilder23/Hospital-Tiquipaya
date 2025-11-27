document.addEventListener("DOMContentLoaded", function () {

    if (!window.__modals) return;

    const open = window.__modals.open;

    const btnOpenCreate = document.getElementById('btn-open-create');
    const modalCreate = document.getElementById('modal-crear-usuario');

    if (btnOpenCreate && modalCreate) {
        btnOpenCreate.addEventListener('click', () => open(modalCreate));
    }

});
