// JavaScript principal para citas de ecografía
// Coordina todas las operaciones CRUD

document.addEventListener('DOMContentLoaded', function() {
    initializeButtons();
    initializeFiltros();
});

function initializeButtons() {
    // Botón abrir modal crear
    const btnOpenCreate = document.getElementById('btn-open-create');
    if (btnOpenCreate) {
        btnOpenCreate.addEventListener('click', function() {
            resetCreateForm();
            new bootstrap.Modal(document.getElementById('modal-create')).show();
        });
    }
}

function initializeFiltros() {
    const inputBusqueda = document.getElementById('buscar-cita');
    const selectEspecialidad = document.getElementById('filtro-especialidad');
    const selectEstado = document.getElementById('filtro-estado');
    const selectEcografo = document.getElementById('filtro-ecografo');
    const selectOrdenFecha = document.getElementById('filtro-orden-fecha');
    const tabla = document.querySelector('.table.citas-ecografia tbody');
    
    if (!tabla) return;
    
    const filas = Array.from(tabla.getElementsByTagName('tr'));

    // Función para normalizar texto (quitar acentos y convertir a minúsculas)
    function normalize(text) {
        return text.normalize('NFD')
                   .replace(/[\u0300-\u036f]/g, '')
                   .toLowerCase()
                   .trim();
    }

    // Función principal de filtrado
    function filtrarTabla() {
        const textoBusqueda = normalize(inputBusqueda ? inputBusqueda.value : '');
        const especialidadSeleccionada = selectEspecialidad ? selectEspecialidad.value : '';
        const estadoSeleccionado = selectEstado ? selectEstado.value : '';
        const ecografoSeleccionado = selectEcografo ? selectEcografo.value : '';
        const ordenFecha = selectOrdenFecha ? selectOrdenFecha.value : '';

        // Filtrar filas
        let filasVisibles = filas.filter(fila => {
            // Saltar fila de "empty"
            if (fila.querySelector('td[colspan]')) return false;

            const paciente = normalize(fila.getAttribute('data-paciente') || '');
            const ci = normalize(fila.getAttribute('data-ci') || '');
            const especialidad = normalize(fila.getAttribute('data-especialidad') || '');
            const ecografo = normalize(fila.getAttribute('data-ecografo') || '');
            const estado = fila.getAttribute('data-estado') || '';
            
            // Buscar en paciente y CI
            const coincideBusqueda = paciente.includes(textoBusqueda) || ci.includes(textoBusqueda);
            
            // Filtrar por especialidad (normalizar ambos para comparar)
            const coincideEspecialidad = !especialidadSeleccionada || especialidad.includes(normalize(especialidadSeleccionada));
            
            // Filtrar por estado
            const coincideEstado = !estadoSeleccionado || estado === estadoSeleccionado;
            
            // Filtrar por ecógrafo (normalizar ambos para comparar)
            const coincideEcografo = !ecografoSeleccionado || ecografo.includes(normalize(ecografoSeleccionado));
            
            return coincideBusqueda && coincideEspecialidad && coincideEstado && coincideEcografo;
        });

        // Ordenar por fecha si es necesario
        if (ordenFecha) {
            filasVisibles.sort((a, b) => {
                const fechaA = new Date(a.getAttribute('data-fecha'));
                const fechaB = new Date(b.getAttribute('data-fecha'));
                
                return ordenFecha === 'desc' ? fechaB - fechaA : fechaA - fechaB;
            });
        }

        // Ocultar todas las filas primero
        filas.forEach(fila => fila.style.display = 'none');

        // Mostrar solo las filas filtradas en el orden correcto
        filasVisibles.forEach((fila, index) => {
            fila.style.display = '';
            // Reordenar en el DOM si es necesario
            if (ordenFecha) {
                tabla.appendChild(fila);
            }
        });
    }

    // Event listeners
    if (inputBusqueda) {
        inputBusqueda.addEventListener('input', filtrarTabla);
    }

    if (selectEspecialidad) {
        selectEspecialidad.addEventListener('change', filtrarTabla);
    }

    if (selectEstado) {
        selectEstado.addEventListener('change', filtrarTabla);
    }

    if (selectEcografo) {
        selectEcografo.addEventListener('change', filtrarTabla);
    }

    if (selectOrdenFecha) {
        selectOrdenFecha.addEventListener('change', filtrarTabla);
    }
}

function resetCreateForm() {
    // Resetear todos los campos del formulario crear
    document.getElementById('search-input').value = '';
    document.getElementById('select-date').value = '';
    document.getElementById('select-doctor').innerHTML = '<option value="">Seleccione un médico</option>';
    document.getElementById('selected-hour').value = '';
    document.getElementById('btn-confirm').classList.add('d-none');
    document.getElementById('create-alert').classList.add('d-none');
    showStep(1);
}

function showStep(stepNumber) {
    // Mostrar solo el step especificado
    document.querySelectorAll('.step').forEach(step => {
        step.classList.add('d-none');
    });
    const stepElement = document.getElementById('step-' + stepNumber);
    if (stepElement) {
        stepElement.classList.remove('d-none');
    }
}

function showAlert(elementId, message, type) {
    // Mostrar alerta en modal específico
    const alert = document.getElementById(elementId);
    if (alert) {
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        alert.classList.remove('d-none');
    }
}

function getCookie(name) {
    // Obtener valor de cookie CSRF
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

// Exportar funciones globales para usar en otros scripts
window.showStep = showStep;
window.showAlert = showAlert;
window.getCookie = getCookie;
window.resetCreateForm = resetCreateForm;
