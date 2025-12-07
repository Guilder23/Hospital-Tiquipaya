// JavaScript para modal de cancelar cita

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
    const btnConfirmDelete = document.getElementById('btn-confirm-delete');
    const modalDelete = new bootstrap.Modal(document.getElementById('modal-delete'));
    const deleteButtons = document.querySelectorAll('.btn-delete');

    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const citaId = this.getAttribute('data-id');
            const paciente = this.getAttribute('data-paciente');
            
            document.getElementById('delete-paciente').textContent = paciente;
            document.getElementById('btn-confirm-delete').setAttribute('data-cita-id', citaId);
            
            modalDelete.show();
        });
    });

    if (btnConfirmDelete) {
        btnConfirmDelete.addEventListener('click', confirmarCancelacion);
    }
});

function confirmarCancelacion() {
    const citaId = this.getAttribute('data-cita-id');

    const formData = new FormData();
    formData.append('estado', 'CANCELADA');

    fetch(`/citas-ecografia/${citaId}/cancelar/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }

        alert('Cita cancelada exitosamente');
        location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al cancelar la cita');
    });
}
