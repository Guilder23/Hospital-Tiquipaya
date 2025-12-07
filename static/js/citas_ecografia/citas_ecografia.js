// JavaScript principal para citas de ecografía
// Coordina todas las operaciones CRUD

document.addEventListener('DOMContentLoaded', function() {
    initializeButtons();
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
