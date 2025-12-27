document.addEventListener('DOMContentLoaded', function() {
    const mCreate = document.getElementById('modal-crear-turno');
    const formCreate = document.getElementById('form-create-turno');
    const btnOpenCreate = document.getElementById('btn-open-create');
    const apiUrl = '/turnos/api/';

    // Funciones Auxiliares (simplificadas, asumiendo que el cierre se maneja con [data-close])
    const openModal = (m) => { if (m) { m.style.display = 'flex'; m.setAttribute('aria-hidden', 'false'); } };
    const closeModal = (m) => { if (m) { m.style.display = 'none'; m.setAttribute('aria-hidden', 'true'); } };
    const getCsrfToken = () => document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Abrir modal
    if (btnOpenCreate) {
        btnOpenCreate.addEventListener('click', () => {
            if (formCreate) formCreate.reset(); 
            openModal(mCreate);
        });
    }

    document.querySelectorAll('[data-close]').forEach(el =>
        el.addEventListener('click', () => closeModal(mCreate))
    );

    // Manejar el submit del formulario
    if (formCreate) {
        formCreate.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const errorDiv = document.getElementById('create-turno-error-message');
            errorDiv.style.display = 'none';
            errorDiv.textContent = '';
            
            const horaIni = formCreate['hora_ini'].value;
            const horaFin = formCreate['hora_fin'].value;
            
            // Validación: hora inicio debe ser menor que hora fin
            if (horaIni >= horaFin) {
                errorDiv.textContent = 'La hora de inicio debe ser menor que la hora de fin';
                errorDiv.style.display = 'block';
                return;
            }
            
            const data = {
                nombre: formCreate['nombre'].value,
                hora_ini: horaIni,
                hora_fin: horaFin,
            };

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                closeModal(mCreate);
                window.location.reload(); 
            } else {
                const errorData = await response.json();
                errorDiv.textContent = 'Error al crear el turno: ' + (errorData.error || 'Error desconocido');
                errorDiv.style.display = 'block';
            }
        });
    }
});