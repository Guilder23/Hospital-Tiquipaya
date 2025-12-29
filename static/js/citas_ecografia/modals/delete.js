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
        btnConfirmDelete.addEventListener('click', function() {
            confirmarCancelacion(modalDelete, btnConfirmDelete);
        });
    }
});

function ensureToastContainer() {
    let container = document.getElementById('ht-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'ht-toast-container';
        container.className = 'ht-toast-container';
        document.body.appendChild(container);
    }
    return container;
}

function showToast(type, title, message) {
    const container = ensureToastContainer();

    const toast = document.createElement('div');
    toast.className = `ht-toast ht-toast-${type}`;

    const icon = type === 'success' ? '✓' : '!';

    toast.innerHTML =
        `<div class="ht-toast-icon">${icon}</div>` +
        '<div class="ht-toast-content">' +
            `<div class="ht-toast-title">${title}</div>` +
            `<div class="ht-toast-message">${message}</div>` +
        '</div>' +
        '<button class="ht-toast-close" type="button">×</button>';

    container.appendChild(toast);

    const closeBtn = toast.querySelector('.ht-toast-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            toast.classList.add('ht-hide');
            setTimeout(() => toast.remove(), 300);
        });
    }

    setTimeout(() => {
        toast.classList.add('ht-hide');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function confirmarCancelacion(modalDelete, btnConfirmDelete) {
    const citaId = btnConfirmDelete.getAttribute('data-cita-id');

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
        if (data.error || data.ok === false) {
            showToast('error', 'Error', data.error || 'No se pudo cancelar la cita');
            return;
        }

        showToast('success', 'Cita cancelada', data.mensaje || 'Cita cancelada exitosamente');
        modalDelete.hide();
        setTimeout(() => location.reload(), 700);
    })
    .catch(error => {
        showToast('error', 'Error', 'Error al cancelar la cita');
    });
}
