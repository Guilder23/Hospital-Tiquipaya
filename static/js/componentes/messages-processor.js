// Procesa mensajes de Django del atributo data-messages en JSON
function processMessages() {
    if (window.__messagesProcessed) return;
    window.__messagesProcessed = true;

    const messagesEl = document.getElementById('django-messages');
    if (!messagesEl) return;

    try {
        const messages = JSON.parse(messagesEl.textContent);
        messages.forEach(msg => {
            if (typeof showNotification === 'function') {
                showNotification(msg.text, msg.type || 'info');
            }
        });
    } catch (e) {
        console.error('Error procesando mensajes:', e);
    }
}

// Ejecutar cuando DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', processMessages);
} else {
    processMessages();
}
