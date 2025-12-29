// JavaScript para modal de editar cita

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
    const btnUpdate = document.getElementById('btn-update');
    const modalEdit = new bootstrap.Modal(document.getElementById('modal-edit'));
    const editButtons = document.querySelectorAll('.btn-edit');

    editButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const citaId = this.getAttribute('data-id');
            cargarDatosEdicion(citaId, modalEdit);
        });
    });

    if (btnUpdate) {
        btnUpdate.addEventListener('click', guardarCambios);
    }
});

function cargarDatosEdicion(citaId, modalEdit) {
    // Obtener datos del data attribute
    const row = document.querySelector(`tr[data-id="${citaId}"]`);
    
    if (!row) {
        showAlert('edit-alert', 'Error: No se encontraron los datos de la cita', 'danger');
        return;
    }

    const paciente = row.getAttribute('data-paciente');
    const ecografo = row.getAttribute('data-ecografo');
    const fecha = row.getAttribute('data-fecha');
    const hora = row.getAttribute('data-hora');
    const estado = row.getAttribute('data-estado');
    const comentario = row.getAttribute('data-comentario') || '';
    const resultado = row.getAttribute('data-resultado') || '';

    // Llenar formulario
    document.getElementById('edit-paciente').value = paciente;
    document.getElementById('edit-medico').value = ecografo;
    document.getElementById('edit-fecha').value = fecha;
    document.getElementById('edit-hora').value = hora;
    document.getElementById('edit-estado').value = estado;
    document.getElementById('edit-comentario').value = comentario;
    document.getElementById('edit-resultado').value = resultado;

    // Guardar ID para uso en guardar
    document.getElementById('btn-update').setAttribute('data-cita-id', citaId);

    // Mostrar modal
    modalEdit.show();
}

function guardarCambios() {
    const citaId = this.getAttribute('data-cita-id');
    const fecha = document.getElementById('edit-fecha').value;
    const hora = document.getElementById('edit-hora').value;
    const estado = document.getElementById('edit-estado').value;
    const comentario = document.getElementById('edit-comentario').value;
    const resultado = document.getElementById('edit-resultado').value;

    if (!fecha || !hora) {
        showAlert('edit-alert', 'Por favor complete los campos requeridos', 'danger');
        return;
    }

    const formData = new FormData();
    formData.append('fecha', fecha);
    formData.append('hora', hora);
    formData.append('estado', estado);
    formData.append('comentario_medico', comentario);
    formData.append('resultado_ecografia', resultado);

    fetch(`/citas-ecografia/${citaId}/editar/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showAlert('edit-alert', data.error, 'danger');
            return;
        }

        showAlert('edit-alert', 'Cita actualizada exitosamente', 'success');
        setTimeout(() => {
            location.reload();
        }, 1500);
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('edit-alert', 'Error al guardar cambios', 'danger');
    });
}

function showAlert(elementId, message, type) {
    const alert = document.getElementById(elementId);
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    alert.classList.remove('d-none');
}
