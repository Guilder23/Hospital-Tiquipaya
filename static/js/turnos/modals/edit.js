document.addEventListener('DOMContentLoaded', function() {
    const mEdit = document.getElementById('modal-editar-turno');
    const formEdit = document.getElementById('form-edit-turno');
    const apiUrl = '/turnos/api/';

    const openModal = (m) => { 
        m.setAttribute('aria-hidden', 'false'); 
        m.style.display = 'flex'; 
    };
    const closeModal = (m) => { 
        m.setAttribute('aria-hidden', 'true');
        m.style.display = 'none'; 
    };
    const getCsrfToken = () => document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.querySelectorAll('[data-close]').forEach(el =>
        el.addEventListener('click', () => closeModal(mEdit))
    );

    // --- ABRIR MODAL Y CARGAR DATOS ---
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = btn.dataset.id;
            const nombre = btn.dataset.nombre;
            const horaIni = btn.dataset.hora_ini;
            const horaFin = btn.dataset.hora_fin;
            const estado = btn.dataset.estado;  // ← NECESARIO

            document.getElementById('edit-id').value = id;
            document.getElementById('edit-nombre').value = nombre;
            document.getElementById('edit-hora_ini').value = horaIni;
            document.getElementById('edit-hora_fin').value = horaFin;

            // ESTADO: true/false → "true"/"false"
            document.getElementById('edit-estado').value = estado === "true" ? "true" : "false";

            openModal(mEdit);
        });
    });

    // --- ENVIAR PATCH ---
    if (formEdit) {
        formEdit.addEventListener('submit', async function(e) {
            e.preventDefault();

            const id = document.getElementById('edit-id').value;

            const data = {
                nombre: formEdit['nombre'].value,
                hora_ini: formEdit['hora_ini'].value,
                hora_fin: formEdit['hora_fin'].value,
                estado: formEdit['estado'].value === "true"  // IMPORTANTÍSIMO
            };

            const response = await fetch(`${apiUrl}${id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                closeModal(mEdit);
                window.location.reload();
            } else {
                const errorData = await response.json();
                console.error('Error al actualizar el turno:', errorData);
            }
        });
    }
});
