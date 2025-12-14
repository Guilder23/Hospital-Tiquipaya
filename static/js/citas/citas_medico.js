// JavaScript para Mis Citas Hoy - Médico

let citaIdActual = null;
let tiempoRealInterval = null;

// Función para obtener cookie CSRF
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

// Función para mostrar alertas
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px; max-width: 400px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    setTimeout(() => alertDiv.remove(), 5000);
}

// Función para actualizar tiempo en tiempo real
function actualizarTiempoReal() {
    document.querySelectorAll('[id^="tiempo-inicio-"]').forEach(el => {
        const now = new Date();
        const ms = String(now.getMilliseconds()).padStart(3, '0');
        const hms = now.toLocaleTimeString('es-ES', { hour12: false });
        el.textContent = hms + '.' + ms;
    });
}

// Inicializar cuando DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Event listener para Iniciar Atención
    document.querySelectorAll('.iniciar-atencion').forEach(btn => {
        btn.addEventListener('click', function() {
            const citaId = this.getAttribute('data-cita-id');
            iniciar_atencion(citaId);
        });
    });

    // Event listener para Finalizar Atención
    document.querySelectorAll('.finalizar-atencion').forEach(btn => {
        btn.addEventListener('click', function() {
            const citaId = this.getAttribute('data-cita-id');
            citaIdActual = citaId;
            const ecoModal = new bootstrap.Modal(document.getElementById('ecoModal'));
            ecoModal.show();
        });
    });


    // Botones del modal de ecografía
    const noEcoBtn = document.getElementById('noEcoButton');
    const siEcoBtn = document.getElementById('siEcoButton');
    const cerrarEcoBtn = document.getElementById('cerrarEcoButton');
    
    if (noEcoBtn) {
        noEcoBtn.addEventListener('click', function() {
            procesar_ecografia(citaIdActual, 'no');
        });
    }

    if (siEcoBtn) {
        siEcoBtn.addEventListener('click', function() {
            procesar_ecografia(citaIdActual, 'si');
        });
    }
    
    // Botón cerrar modal (solo cierra sin hacer nada)
    if (cerrarEcoBtn) {
        cerrarEcoBtn.addEventListener('click', function() {
            const ecoModal = bootstrap.Modal.getInstance(document.getElementById('ecoModal'));
            if (ecoModal) {
                ecoModal.hide();
            }
        });
    }

    // Actualizar hora con milisegundos en tiempo real cada 100ms
    tiempoRealInterval = setInterval(actualizarTiempoReal, 100);
});

// Función para iniciar atención
function iniciar_atencion(citaId) {
    const formData = new FormData();
    formData.append('accion', 'iniciar');

    fetch(`/citas/${citaId}/iniciar/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            showAlert('success', 'Atención iniciada');
            setTimeout(() => location.reload(), 1000);
        } else {
            showAlert('danger', data.error || 'Error al iniciar atención');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Error en la solicitud');
    });
}

// Función para procesar ecografía
function procesar_ecografia(citaId, habilitar) {
    console.log('Procesando ecografía:', { citaId, habilitar });
    
    const formData = new FormData();
    formData.append('habilitar', habilitar);
    
    // Si se habilita, obtener datos del formulario
    if (habilitar === 'si') {
        const ecografiaSelect = document.getElementById('ecoEcografia');
        const comentarioTextarea = document.getElementById('ecoComentario');
        
        console.log('Elementos encontrados:', {
            ecografiaSelect: !!ecografiaSelect,
            comentarioTextarea: !!comentarioTextarea
        });
        
        if (!ecografiaSelect || !comentarioTextarea) {
            showAlert('danger', 'Error: No se encontraron los campos del formulario');
            console.error('No se encontraron los elementos del formulario');
            return;
        }
        
        const ecografiaId = ecografiaSelect.value;
        const comentario = comentarioTextarea.value;
        
        console.log('Valores capturados del formulario:', {
            ecografiaId: ecografiaId,
            comentario: comentario,
            ecografiaIdType: typeof ecografiaId,
            comentarioType: typeof comentario
        });
        
        if (!ecografiaId || ecografiaId === '') {
            showAlert('danger', 'Por favor selecciona una ecografía');
            return;
        }
        
        if (!comentario || !comentario.trim()) {
            showAlert('danger', 'Por favor ingresa un comentario');
            return;
        }
        
        formData.append('ecografia', ecografiaId);
        formData.append('comentario', comentario);
        
        console.log('FormData preparado:');
        for (let [key, value] of formData.entries()) {
            console.log(`  ${key}: ${value}`);
        }
    }

    console.log('Enviando request a /citas/' + citaId + '/procesar-ecografia/');
    
    fetch(`/citas/${citaId}/procesar-ecografia/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(response => {
        console.log('Respuesta recibida:', response.status);
        if (!response.ok) {
            return response.json().then(err => {
                console.error('Error response:', err);
                throw new Error(`HTTP ${response.status}: ${err.error || 'Error desconocido'}`);
            }).catch(e => {
                throw new Error(`HTTP ${response.status}: Error al parsear respuesta`);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Datos procesados:', data);
        
        if (data.ok) {
            // Cerrar modal de ecografía
            try {
                const ecoModal = bootstrap.Modal.getInstance(document.getElementById('ecoModal'));
                if (ecoModal) {
                    ecoModal.hide();
                }
            } catch(e) {
                console.log('Nota: Modal de eco no estaba abierto:', e.message);
            }

            if (habilitar === 'si') {
                showAlert('success', 'Ecografía habilitada correctamente');
            } else {
                showAlert('success', 'Paciente atendido sin ecografía');
            }

            setTimeout(() => location.reload(), 2000);
        } else {
            console.error('Error en respuesta:', data);
            showAlert('danger', data.error || 'Error al procesar ecografía');
        }
    })
    .catch(error => {
        console.error('Error en solicitud:', error);
        showAlert('danger', 'Error en la solicitud: ' + error.message);
    });
}

