/* Notifications System */

function showNotification(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast-notification ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showWarning(message) {
    showNotification(message, 'warning');
}

function showInfo(message) {
    showNotification(message, 'info');
}

// Mostrar mensajes de Django al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('[data-message]');
    messages.forEach(el => {
        const msg = el.getAttribute('data-message');
        const type = el.getAttribute('data-type') || 'info';
        showNotification(msg, type);
        el.remove();
    });
});
