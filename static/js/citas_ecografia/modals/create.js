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
    const btnSearch = document.getElementById('btn-search');
    const btnBackSearch = document.getElementById('btn-back-search');
    const btnBackPatient = document.getElementById('btn-back-patient');
    const btnBackDoctor = document.getElementById('btn-back-doctor');
    const btnConfirm = document.getElementById('btn-confirm');
    const selectDoctor = document.getElementById('select-doctor');
    const searchInput = document.getElementById('search-input');

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

    // Cambio de médico/ecógrafo
    if (selectDoctor) {
        selectDoctor.addEventListener('change', seleccionarEcografo);
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
    document.getElementById('select-doctor').innerHTML = '<option value="">Seleccione un ecógrafo</option>';
    document.getElementById('selected-hour').value = '';
    document.getElementById('selected-date').value = '';
    document.getElementById('horarios-container').innerHTML = '';
    document.getElementById('calendario-container').innerHTML = '';
    document.getElementById('step-3b').classList.add('d-none');
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
        document.getElementById('patient-ecografia').textContent = data.ecografia_asignada || '-';
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
                btnNext.textContent = 'Seleccionar Fecha y Ecografo';
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
    formData.append('ecografo_id', citaEcografiaData.ecografo_id);
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
    document.getElementById('select-doctor').innerHTML = '<option value="">Seleccione un ecógrafo</option>';
    document.getElementById('selected-hour').value = '';
    document.getElementById('selected-date').value = '';
    document.getElementById('horarios-container').innerHTML = '';
    document.getElementById('calendario-container').innerHTML = '';
    document.getElementById('step-3b').classList.add('d-none');
    document.getElementById('btn-confirm').classList.add('d-none');
    document.getElementById('create-alert').classList.add('d-none');
    showStep(1);
}

function showAlert(elementId, message, type) {
    const alert = document.getElementById(elementId);
    alert.className = `alert alert-${type} d-block`;
    alert.textContent = message;
}

function seleccionarEcografo() {
    const selectDoctor = document.getElementById('select-doctor');
    const ecoId = selectDoctor.value;
    
    if (!ecoId) {
        document.getElementById('step-3b').classList.add('d-none');
        return;
    }
    
    // Obtener información del ecógrafo (contrato, días de atención, turnos)
    fetch(`/citas-ecografia/api/ecografo/${ecoId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data || data.error) {
            showAlert('create-alert', data.error || 'Error al cargar información del ecógrafo', 'danger');
            return;
        }

        citaEcografiaData.ecografo_id = ecoId;
        citaEcografiaData.ecografo = data;
        
        // Validar que exista contrato
        if (!data.contrato_inicio || !data.contrato_fin) {
            showAlert('create-alert', 'El ecógrafo no tiene un contrato asignado', 'warning');
            return;
        }

        // Mostrar información del contrato
        const contratoInfo = document.getElementById('eco-contrato-info');
        const fechaInicio = new Date(data.contrato_inicio).toLocaleDateString('es-ES');
        const fechaFin = new Date(data.contrato_fin).toLocaleDateString('es-ES');
        contratoInfo.innerHTML = `
            <strong>${data.nombre}</strong><br>
            Contrato: ${fechaInicio} a ${fechaFin}<br>
            Días: ${data.dias_trabajo.join(', ')}
        `;
        
        // Generar calendario
        generarCalendario(data);
        
        // Mostrar sección 3b
        document.getElementById('step-3b').classList.remove('d-none');
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('create-alert', 'Error al cargar información del ecógrafo', 'danger');
    });
}

function generarCalendario(ecografo) {
    const container = document.getElementById('calendario-container');
    container.innerHTML = '';
    
    if (!ecografo.contrato_inicio || !ecografo.contrato_fin) {
        container.innerHTML = '<p class="text-danger">No hay contrato disponible para este ecógrafo</p>';
        return;
    }
    
    try {
        const fechaInicio = new Date(ecografo.contrato_inicio);
        const fechaFin = new Date(ecografo.contrato_fin);
        const diasTrabajo = ecografo.dias_trabajo_numeros; // [0=lunes, 1=martes, etc]
        
        const contenedorGral = document.createElement('div');
        contenedorGral.className = 'calendario-container';
        
        // Crear encabezados de días (constantes para todos los meses)
        const headerDiv = document.createElement('div');
        headerDiv.className = 'calendario-header';
        const diasNombre = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
        diasNombre.forEach(dia => {
            const headerDay = document.createElement('div');
            headerDay.textContent = dia;
            headerDiv.appendChild(headerDay);
        });
        contenedorGral.appendChild(headerDiv);
        
        // Iterar por meses
        let fechaActual = new Date(fechaInicio.getFullYear(), fechaInicio.getMonth(), 1);
        
        while (fechaActual <= fechaFin) {
            const mesMoment = new Date(fechaActual);
            
            // Crear contenedor del mes
            const mesDiv = document.createElement('div');
            mesDiv.className = 'calendario-mes';
            
            // Título del mes
            const mesTitle = document.createElement('div');
            mesTitle.className = 'calendario-mes-titulo';
            const opciones = { month: 'long', year: 'numeric' };
            mesTitle.textContent = mesMoment.toLocaleDateString('es-ES', opciones);
            mesDiv.appendChild(mesTitle);
            
            // Grid del mes
            const gridDiv = document.createElement('div');
            gridDiv.className = 'calendario-grid';
            
            // Encontrar el primer lunes del mes
            let primerDia = new Date(mesMoment.getFullYear(), mesMoment.getMonth(), 1);
            let diaSemana = (primerDia.getDay() + 6) % 7; // 0=lunes
            
            // Agregar celdas vacías al inicio
            for (let i = 0; i < diaSemana; i++) {
                const celda = document.createElement('div');
                celda.className = 'fecha-btn fecha-vacia';
                gridDiv.appendChild(celda);
            }
            
            // Agregar días del mes
            const ultimoDia = new Date(mesMoment.getFullYear(), mesMoment.getMonth() + 1, 0).getDate();
            
            for (let dia = 1; dia <= ultimoDia; dia++) {
                const fecha = new Date(mesMoment.getFullYear(), mesMoment.getMonth(), dia);
                
                // Verificar si está en el rango del contrato
                const estaEnRango = fecha >= fechaInicio && fecha <= fechaFin;
                
                // Obtener día de la semana normalizado
                let diaSemanaNormalizado = (fecha.getDay() + 6) % 7; // 0=lunes
                const esHabilitado = diasTrabajo.includes(diaSemanaNormalizado);
                
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'fecha-btn';
                btn.textContent = dia;
                btn.dataset.fecha = fecha.toISOString().split('T')[0];
                
                // Deshabilitar si no está en rango, no es día habilitado, o es fecha pasada
                const hoy = new Date();
                hoy.setHours(0, 0, 0, 0);
                
                if (!estaEnRango || !esHabilitado || fecha < hoy) {
                    btn.disabled = true;
                } else {
                    btn.addEventListener('click', () => seleccionarFecha(btn));
                }
                
                gridDiv.appendChild(btn);
            }
            
            mesDiv.appendChild(gridDiv);
            contenedorGral.appendChild(mesDiv);
            
            // Pasar al siguiente mes
            fechaActual.setMonth(fechaActual.getMonth() + 1);
            
            // Parar si ya pasamos el mes de fin
            if (fechaActual > fechaFin) {
                break;
            }
        }
        
        container.appendChild(contenedorGral);
    } catch (error) {
        console.error('Error generando calendario:', error);
        container.innerHTML = '<p class="text-danger">Error al generar el calendario</p>';
    }
}

function seleccionarFecha(btn) {
    // Remover selección anterior
    document.querySelectorAll('#calendario-container .fecha-btn.selected').forEach(b => {
        b.classList.remove('selected');
    });
    
    // Marcar como seleccionado
    btn.classList.add('selected');
    const fecha = btn.dataset.fecha;
    document.getElementById('selected-date').value = fecha;
    
    // Cargar horarios disponibles para ese día
    cargarHorariosDelDia(fecha);
}

function cargarHorariosDelDia(fecha) {
    // Obtener turnos del ecógrafo para ese día
    const ecografo = citaEcografiaData.ecografo;
    
    // Los turnos del ecógrafo son los mismos para todos sus días de atención
    const turnosDelDia = ecografo.turnos;
    
    if (!turnosDelDia || turnosDelDia.length === 0) {
        showAlert('create-alert', 'No hay turnos disponibles para este ecógrafo', 'warning');
        return;
    }
    
    // Mostrar paso 4
    showStep(4);
    
    // Generar horarios
    generarHorarios(turnosDelDia, fecha);
}

function generarHorarios(turnos, fecha) {
    const container = document.getElementById('horarios-container');
    container.innerHTML = '';
    
    if (!turnos || turnos.length === 0) {
        container.innerHTML = '<p class="text-warning">No hay turnos disponibles</p>';
        return;
    }
    
    turnos.forEach(turno => {
        const horaInicio = turno.hora_ini;
        const horaFin = turno.hora_fin;
        
        // Convertir strings HH:MM a minutos
        const [hiHora, hiMin] = horaInicio.split(':');
        const [hfHora, hfMin] = horaFin.split(':');
        
        let minutoInicio = parseInt(hiHora) * 60 + parseInt(hiMin);
        let minutoFin = parseInt(hfHora) * 60 + parseInt(hfMin);
        
        // Generar slots de 30 minutos
        while (minutoInicio < minutoFin) {
            const horas = Math.floor(minutoInicio / 60);
            const minutos = minutoInicio % 60;
            const horaSlot = `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}`;
            
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'horario-btn horario-free';
            btn.textContent = horaSlot;
            btn.dataset.hora = horaSlot;
            btn.dataset.turnoId = turno.id;
            btn.addEventListener('click', () => seleccionarHora(btn, fecha, horaSlot));
            
            container.appendChild(btn);
            
            // Incrementar 30 minutos
            minutoInicio += 30;
        }
    });
}

function seleccionarHora(btn, fecha, horaSlot) {
    // Remover selección anterior
    document.querySelectorAll('#horarios-container .horario-btn.selected').forEach(b => {
        b.classList.remove('selected');
    });
    
    // Marcar como seleccionado
    btn.classList.add('selected');
    document.getElementById('selected-hour').value = horaSlot;
    document.getElementById('selected-date').value = fecha;
    
    // Guardar información en el objeto global
    citaEcografiaData.fecha = fecha;
    citaEcografiaData.hora = horaSlot;
    
    // Mostrar botón de confirmación
    document.getElementById('btn-confirm').classList.remove('d-none');
}
