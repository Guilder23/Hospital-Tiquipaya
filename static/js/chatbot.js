class ChatBot {
  constructor() {
    this.chatWindow = null;
    this.messageContainer = null;
    this.inputField = null;
    this.sendButton = null;
    this.responses = [];
    this.conversationHistory = [];
    
    this.init();
  }
  
  async init() {
    // Cargar respuestas predefinidas
    try {
      const response = await fetch('/static/data/chatbot-responses.json');
      this.responses = await response.json();
    } catch (error) {
      console.error('Error cargando respuestas:', error);
      this.responses = { responses: [] };
    }
    
    // Esperar a que el DOM esté listo
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setupUI());
    } else {
      this.setupUI();
    }
  }
  
  setupUI() {
    // Crear estructura del chatbot si no existe
    if (!document.getElementById('chatbot-widget')) {
      this.createChatbotHTML();
    }
    
    // Obtener referencias a elementos
    this.chatWindow = document.getElementById('chatbot-window');
    this.messageContainer = document.getElementById('chatbot-messages');
    this.inputField = document.getElementById('chatbot-input');
    this.sendButton = document.getElementById('chatbot-send');
    
    // Agregar event listeners
    document.getElementById('chatbot-toggle').addEventListener('click', () => this.toggleChat());
    document.getElementById('chatbot-close').addEventListener('click', () => this.closeChat());
    this.sendButton.addEventListener('click', () => this.sendMessage());
    this.inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });
    
    // Event listeners para quick suggestions
    document.querySelectorAll('.quick-suggestion-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const message = e.target.dataset.message;
        this.inputField.value = message;
        this.sendMessage();
      });
    });
    
    // Mensaje inicial
    setTimeout(() => this.addBotMessage("¡Hola! 👋 Bienvenido a Hospital Tiquipaya. Soy tu asistente virtual. ¿En qué puedo ayudarte?"), 500);
  }
  
  createChatbotHTML() {
    const html = `
      <div class="chatbot-widget" id="chatbot-widget">
        <button class="chatbot-toggle" id="chatbot-toggle" title="Abrir chat">
          🤖
        </button>
        
        <div class="chatbot-window" id="chatbot-window">
          <div class="chatbot-header">
            <div>
              <h3>Hospital Tiquipaya</h3>
              <p>Asistente Virtual</p>
            </div>
            <button class="chatbot-close" id="chatbot-close">✕</button>
          </div>
          
          <div class="chatbot-messages" id="chatbot-messages"></div>
          
          <div class="chatbot-quick-suggestions">
            <div class="quick-suggestions-list" id="quick-suggestions-list">
              <button class="quick-suggestion-btn" data-message="¿Cómo agendo una cita?">¿Cómo agendo?</button>
              <button class="quick-suggestion-btn" data-message="¿Cuál es el horario?">Horarios</button>
              <button class="quick-suggestion-btn" data-message="¿Qué especialidades hay?">Especialidades</button>
              <button class="quick-suggestion-btn" data-message="Ubicación del hospital">Ubicación</button>
              <button class="quick-suggestion-btn" data-message="¿Cuáles son los requisitos?">Requisitos</button>
              <button class="quick-suggestion-btn" data-message="¿Cómo contacto?">Contacto</button>
            </div>
          </div>
          
          <div class="chatbot-input-area">
            <input 
              type="text" 
              class="chatbot-input" 
              id="chatbot-input" 
              placeholder="Escribe tu pregunta..."
              autocomplete="off"
            >
            <button class="chatbot-send" id="chatbot-send" title="Enviar">
              ➤
            </button>
          </div>
        </div>
      </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', html);
  }
  
  toggleChat() {
    this.chatWindow.classList.toggle('active');
    if (this.chatWindow.classList.contains('active')) {
      this.inputField.focus();
    }
  }
  
  closeChat() {
    this.chatWindow.classList.remove('active');
  }
  
  addUserMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    messageDiv.innerHTML = `<div class="message-content">${this.escapeHtml(text)}</div>`;
    this.messageContainer.appendChild(messageDiv);
    this.scrollToBottom();
  }
  
  addBotMessage(text, buttons = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    
    let contentHTML = `
      <div class="message-avatar">🤖</div>
      <div class="message-content">
        ${this.formatMessage(text)}
    `;
    
    if (buttons && buttons.length > 0) {
      contentHTML += '<div class="message-buttons">';
      buttons.forEach(btn => {
        if (btn.link) {
          contentHTML += `<a href="${btn.link}" class="message-button link">${this.escapeHtml(btn.text)}</a>`;
        } else {
          contentHTML += `<button class="message-button" onclick="chatBot.sendPredefinedMessage('${this.escapeHtml(btn.text)}')">${this.escapeHtml(btn.text)}</button>`;
        }
      });
      contentHTML += '</div>';
    }
    
    contentHTML += '</div>';
    messageDiv.innerHTML = contentHTML;
    this.messageContainer.appendChild(messageDiv);
    this.scrollToBottom();
  }
  
  addTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    messageDiv.innerHTML = `
      <div class="message-avatar">🤖</div>
      <div class="message-content typing-indicator">
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
        <span class="typing-dot"></span>
      </div>
    `;
    messageDiv.id = 'typing-indicator';
    this.messageContainer.appendChild(messageDiv);
    this.scrollToBottom();
  }
  
  removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }
  
  sendMessage() {
    const text = this.inputField.value.trim();
    
    if (!text) return;
    
    // Agregar mensaje del usuario
    this.addUserMessage(text);
    this.inputField.value = '';
    
    // Guardar en historial
    this.conversationHistory.push({ role: 'user', content: text });
    
    // Mostrar indicador de escritura
    this.addTypingIndicator();
    
    // Simular delay de respuesta (para que parezca más natural)
    setTimeout(() => {
      this.removeTypingIndicator();
      this.getResponse(text);
    }, 800 + Math.random() * 400);
  }
  
  sendPredefinedMessage(text) {
    this.inputField.value = text;
    this.sendMessage();
  }
  
  getResponse(userMessage) {
    const lowerMessage = userMessage.toLowerCase();
    
    // Buscar respuesta basada en palabras clave
    let botResponse = null;
    
    for (const item of this.responses.responses) {
      for (const keyword of item.keywords) {
        if (lowerMessage.includes(keyword.toLowerCase())) {
          botResponse = item;
          break;
        }
      }
      if (botResponse) break;
    }
    
    // Si no encuentra coincidencia
    if (!botResponse) {
      botResponse = {
        response: "Disculpa, no entiendo bien tu pregunta. 🤔\n\nPuedo ayudarte con:\n• Agendar citas\n• Horarios de atención\n• Especialidades\n• Ubicación y contacto\n• Requisitos para agendar\n\n¿Cuál de estos temas te interesa?",
        buttons: [
          { text: "Agendar cita" },
          { text: "Horarios" },
          { text: "Especialidades" }
        ]
      };
    }
    
    // Agregar respuesta del bot
    this.addBotMessage(botResponse.response, botResponse.buttons || null);
    
    // Guardar en historial
    this.conversationHistory.push({ role: 'bot', content: botResponse.response });
  }
  
  scrollToBottom() {
    setTimeout(() => {
      this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }, 0);
  }
  
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  formatMessage(text) {
    // Reemplazar saltos de línea
    let formatted = text.replace(/\n/g, '<br>');
    
    // Hacer bold para **texto**
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Hacer itálica para *texto*
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    return formatted;
  }
}

// Instanciar chatbot cuando se carga la página
let chatBot;
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    chatBot = new ChatBot();
  });
} else {
  chatBot = new ChatBot();
}
