// JavaScript para modal de crear cita de ecografía

let citaEcografiaData = {};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const btnOpenCreate = document.getElementById('btn-open-create');
    const btnSearch = document.getElementById('btn-search');
    const btnBackSearch = document.getElementById('btn-back-search');
    const btnBackPatient = document.getElementById('btn-back-patient');
    const btnBackDoctor = document.getElementById('btn-back-doctor');
    const btnConfirm = document.getElementById('btn-confirm');
    const selectDate = document.getElementById('select-date');
    const selectDoctor = document.getElementById('select-doctor');
    const searchInput = document.getElementById('search-input');
    const modalCreate = new bootstrap.Modal(document.getElementById('modal-create'));

    // Abrir modal
    if (btnOpenCreate) {
        btnOpenCreate.addEventListener('click', () => {
            citaEcografiaData = {};
            resetCreateForm();
            modalCreate.show();
        });
    }

    // Buscar paciente
    if (btnSearch) {
        btnSearch.addEventListener('click', buscarPaciente);
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') buscarPaciente();
            });
        }
    }

    // Volver a búsqueda
    if (btnBackSearch) {
        btnBackSearch.addEventListener('click', () => {
            showStep(1);
            resetCreateForm();
        });
    }

    // Volver a paciente
    if (btnBackPatient) {
        btnBackPatient.addEventListener('click', () => {
            showStep(2);
        });
    }

    // Cambio de fecha
    if (selectDate) {
        selectDate.addEventListener('change', cargarMedicosDisponibles);
    }

    // Cambio de médico
    if (selectDoctor) {
        selectDoctor.addEventListener('change', cargarHorarios);
    }

    // Volver a médico
    if (btnBackDoctor) {
        btnBackDoctor.addEventListener('click', () => {
            showStep(3);
            document.getElementById('selected-hour').value = '';
            btnConfirm.classList.add('d-none');
        });
    }

    // Confirmar cita
    if (btnConfirm) {
        btnConfirm.addEventListener('click', agendarCita);
    }
});

function buscarPaciente() {
    const searchInput = document.getElementById('search-input');
    const searchTerm = searchInput.value.trim();
    
    if (!searchTerm) {
        showAlert('create-alert', 'Por favor ingrese el CI del paciente', 'danger');
        return;
    }

    // Limpiar pasos 3 y 4 si existen datos previos
    document.getElementById('select-date').value = '';
    document.getElementById('select-doctor').innerHTML = '<option value="">Seleccione un médico</option>';
    document.getElementById('selected-hour').value = '';
    document.getElementById('horarios-container').innerHTML = '';
    document.getElementById('btn-confirm').classList.add('d-none');

    fetch('/citas-ecografia/buscar-paciente/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ search: searchTerm })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert('create-alert', data.error, 'danger');
            return;
        }

        citaEcografiaData.paciente = data.paciente;
        citaEcografiaData.paciente_id = data.paciente.id;

        document.getElementById('patient-names').textContent = `${data.paciente.nombres} ${data.paciente.apellido_paterno}`;
        document.getElementById('patient-ci').textContent = data.paciente.ci;
        document.getElementById('patient-specialty').textContent = data.especialidad_nombre || '-';
        document.getElementById('patient-comment').textContent = data.comentario_medico || '-';

        // Guardar médicos disponibles en el objeto global
        citaEcografiaData.medicos_disponibles = data.medicos_disponibles || [];

        showStep(2);

        // Mostrar botón para avanzar a selección de fecha/médico solo si está habilitado
        if (data.habilitado) {
            if (!document.getElementById('btn-next-patient')) {
                const btnNext = document.createElement('button');
                btnNext.type = 'button';
                btnNext.className = 'btn btn-primary ms-2';
                btnNext.id = 'btn-next-patient';
                btnNext.textContent = 'Seleccionar Fecha y Médico';
                btnNext.onclick = function() {
                    showStep(3);
                    cargarMedicosEspecialidad();
                };
                document.getElementById('step-2').appendChild(btnNext);
            }
        } else {
            if (document.getElementById('btn-next-patient')) {
                document.getElementById('btn-next-patient').remove();
            }
            showAlert('create-alert', 'Este paciente no tiene habilitada la ecografía', 'warning');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('create-alert', 'Error al buscar el paciente', 'danger');
    });
}

function cargarMedicosEspecialidad() {
    const selectDoctor = document.getElementById('select-doctor');
    selectDoctor.innerHTML = '<option value="">Seleccione un médico</option>';
    if (citaEcografiaData.medicos_disponibles && citaEcografiaData.medicos_disponibles.length > 0) {
        citaEcografiaData.medicos_disponibles.forEach(medico => {
            const option = document.createElement('option');
            option.value = medico.id;
            option.textContent = medico.nombre;
            selectDoctor.appendChild(option);
        });
    }
}

function cargarMedicosDisponibles() {
    const fecha = document.getElementById('select-date').value;
    if (!fecha) return;
    citaEcografiaData.fecha = fecha;
}

function cargarHorarios() {
    const medicoId = document.getElementById('select-doctor').value;
    const fecha = citaEcografiaData.fecha;

    if (!medicoId || !fecha) return;

    citaEcografiaData.medico_id = medicoId;
    const selectDoctorEl = document.getElementById('select-doctor');
    const medicoNombre = selectDoctorEl && selectDoctorEl.options[selectDoctorEl.selectedIndex] ? selectDoctorEl.options[selectDoctorEl.selectedIndex].textContent : '';
    citaEcografiaData.medico_nombre = medicoNombre;

    const formData = new FormData();
    formData.append('medico_id', medicoId);
    formData.append('fecha', fecha);

    fetch('/citas-ecografia/obtener-horarios/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert('create-alert', data.error, 'danger');
            return;
        }

        const slots = [];
        if (data.horarios) {
            Object.values(data.horarios).forEach(lista => {
                lista.forEach(item => {
                    slots.push({ hora: item.hora, disponible: !!item.disponible });
                });
            });
        }

        if (data.mensaje) {
            showAlert('create-alert', data.mensaje, 'success');
        }

        mostrarHorarios(slots);
        // Mostrar resumen de selección (fecha y médico)
        try {
            const d = new Date(fecha);
            const fechaStr = isNaN(d.getTime()) ? fecha : d.toLocaleDateString('es-ES', { weekday:'long', year:'numeric', month:'long', day:'numeric' });
            const sd = document.getElementById('summary-date');
            const sm = document.getElementById('summary-doctor');
            if (sd) sd.textContent = fechaStr;
            if (sm) sm.textContent = medicoNombre || '-';
        } catch(e) {}
        showStep(4);
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('create-alert', 'Error al cargar horarios', 'danger');
    });
}

function mostrarHorarios(slots) {
    const container = document.getElementById('horarios-container');
    container.innerHTML = '';

    slots.forEach(slot => {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = slot.hora;
        button.classList.add('horario-btn');
        if (slot.disponible) {
            button.classList.add('horario-free');
            button.setAttribute('title','Horario libre');
            button.addEventListener('click', () => {
                document.querySelectorAll('.horario-btn.horario-free').forEach(btn => {
                    btn.classList.remove('selected');
                });
                button.classList.add('selected');
                document.getElementById('selected-hour').value = slot.hora;
                document.getElementById('btn-confirm').classList.remove('d-none');
            });
        } else {
            button.classList.add('horario-busy');
            button.disabled = true;
            button.setAttribute('title','Horario ocupado');
            button.setAttribute('aria-disabled','true');
        }
        container.appendChild(button);
    });
}

function agendarCita() {
    const hora = document.getElementById('selected-hour').value;

    if (!hora) {
        showAlert('create-alert', 'Por favor seleccione una hora', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('paciente_id', citaEcografiaData.paciente_id);
    formData.append('medico_id', citaEcografiaData.medico_id);
    formData.append('fecha', citaEcografiaData.fecha);
    formData.append('hora', hora);

    fetch('/citas-ecografia/crear/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert('create-alert', data.error, 'danger');
            return;
        }

        showAlert('create-alert', 'Cita agendada exitosamente', 'success');
        setTimeout(() => {
            location.reload();
        }, 1500);
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('create-alert', 'Error al agendar la cita', 'danger');
    });
}

function showStep(stepNumber) {
    // Mostrar todos los pasos hasta el step actual
    for (let i = 1; i <= 4; i++) {
        const step = document.getElementById('step-' + i);
        if (i <= stepNumber) {
            step.classList.remove('d-none');
        } else {
            step.classList.add('d-none');
        }
    }
    
    // Scroll al final del modal para ver el paso actual
    const modalBody = document.querySelector('#modal-create .modal-body');
    setTimeout(() => {
        modalBody.scrollTop = modalBody.scrollHeight;
    }, 100);
}

function resetCreateForm() {
    document.getElementById('search-input').value = '';
    document.getElementById('select-date').value = '';
    document.getElementById('select-doctor').innerHTML = '<option value="">Seleccione un médico</option>';
    document.getElementById('selected-hour').value = '';
    document.getElementById('btn-confirm').classList.add('d-none');
    document.getElementById('create-alert').classList.add('d-none');
    showStep(1);
}

function showAlert(elementId, message, type) {
    const alert = document.getElementById(elementId);
    alert.className = `alert alert-${type} d-block`;
    alert.textContent = message;
}
