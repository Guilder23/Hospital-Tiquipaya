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

    // ========== VALIDACIONES EN TIEMPO REAL ==========
    // Validar nombre: solo caracteres alfabéticos
    const nombreInput = document.getElementById('edit-nombre');
    if(nombreInput){
        nombreInput.addEventListener('input', function() {
            const regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g;
            if (regex.test(this.value)) {
                this.value = this.value.replace(regex, '');
            }
        });
    }

    // Validar horas: hora inicio no puede ser >= hora fin (en tiempo real)
    const horaIniInput = document.getElementById('edit-hora_ini');
    const horaFinInput = document.getElementById('edit-hora_fin');
    
    function validarHorasTurnoEdit() {
        if(horaIniInput && horaFinInput && horaIniInput.value && horaFinInput.value) {
            if(horaIniInput.value >= horaFinInput.value) {
                horaFinInput.setCustomValidity('La hora de fin debe ser mayor que la hora de inicio');
            } else {
                horaFinInput.setCustomValidity('');
            }
        }
    }
    
    if(horaIniInput) horaIniInput.addEventListener('change', validarHorasTurnoEdit);
    if(horaFinInput) horaFinInput.addEventListener('change', validarHorasTurnoEdit);

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

            const errorDiv = document.getElementById('edit-turno-error-message');
            errorDiv.style.display = 'none';
            errorDiv.textContent = '';

            const id = document.getElementById('edit-id').value;
            const horaIni = formEdit['hora_ini'].value;
            const horaFin = formEdit['hora_fin'].value;
            
            // Validación: hora inicio debe ser menor que hora fin
            if (horaIni >= horaFin) {
                errorDiv.textContent = 'La hora de inicio debe ser menor que la hora de fin';
                errorDiv.style.display = 'block';
                return;
            }

            const data = {
                nombre: formEdit['nombre'].value,
                hora_ini: horaIni,
                hora_fin: horaFin,
                estado: formEdit['estado'].value === "true"
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
                errorDiv.textContent = 'Error al actualizar el turno: ' + (errorData.error || 'Error desconocido');
                errorDiv.style.display = 'block';
            }
        });
    }
});
