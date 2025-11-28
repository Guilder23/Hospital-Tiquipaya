document.addEventListener('DOMContentLoaded', function() {
    const mDelete = document.getElementById('modal-eliminar-turno');
    const btnConfirmDelete = document.getElementById('btn-confirm-delete');
    const apiUrl = '/turnos/api/';

    const openModal = (m) => { m.style.display = 'flex'; m.setAttribute('aria-hidden', 'false'); };
    const closeModal = (m) => { m.style.display = 'none'; m.setAttribute('aria-hidden', 'true'); };
    const getCsrfToken = () => document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.querySelectorAll('[data-close]').forEach(el =>
        el.addEventListener('click', () => closeModal(mDelete))
    );

    // --- ABRIR MODAL ---
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function() {

            const id = btn.dataset.id;
            const nombre = btn.dataset.nombre;
            const estado = btn.dataset.estado; // ← NECESARIO

            document.getElementById('delete-id').value = id;
            document.getElementById('delete-nombre').textContent = nombre;
            document.getElementById('delete-estado').value = estado;

            const title = document.getElementById('modal-title-estado');
            const accion = document.getElementById('accion-text');

            if (estado === "true") {
                title.textContent = "Deshabilitar Turno";
                accion.textContent = "deshabilitar";
                btnConfirmDelete.textContent = "Deshabilitar";
            } else {
                title.textContent = "Habilitar Turno";
                accion.textContent = "habilitar";
                btnConfirmDelete.textContent = "Habilitar";
            }

            openModal(mDelete);
        });
    });

    // --- CONFIRMAR ---
    btnConfirmDelete.addEventListener('click', async function() {

        const id = document.getElementById('delete-id').value;
        const estadoActual = document.getElementById('delete-estado').value;

        let method, body;

        if (estadoActual === "true") {
            // DESHABILITAR
            method = "PATCH";
            body = JSON.stringify({ estado: false });

        } else {
            // HABILITAR
            method = "PATCH";
            body = JSON.stringify({ estado: true });
        }

        const response = await fetch(`${apiUrl}${id}/`, {
            method,
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            },
            body
        });

        if (response.ok) {
            closeModal(mDelete);
            window.location.reload();
        } else {
            alert("Error al actualizar el estado del turno.");
        }
    });
});
