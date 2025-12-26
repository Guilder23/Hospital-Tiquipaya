// ======= HOSPITAL TIQUIPAYA - HOME PAGE SCRIPTS =======

document.addEventListener('DOMContentLoaded', function() {
  initCounters();
  initCarousel();
  initSmoothScroll();
});

// ======= COUNTER ANIMATION =======
function initCounters() {
  const counters = document.querySelectorAll('.count-up');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.animated) {
        const target = parseInt(entry.target.getAttribute('data-target'));
        animateCount(entry.target, target);
        entry.target.dataset.animated = 'true';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => observer.observe(counter));
}

function animateCount(element, target) {
  let count = 0;
  const increment = target / 50;
  const duration = 1500;
  const startTime = Date.now();

  function updateCount() {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    count = Math.ceil(target * easeOutQuart(progress));
    
    if (target === 100) {
      element.innerText = count + '%';
    } else {
      element.innerText = count + '+';
    }
    
    if (progress < 1) {
      requestAnimationFrame(updateCount);
    }
  }
  
  updateCount();
}

function easeOutQuart(t) {
  return 1 - Math.pow(1 - t, 4);
}

// ======= SPECIALISTS CAROUSEL =======
function initCarousel() {
  const grid = document.getElementById('specialistsGrid');
  const prevBtn = document.getElementById('prevSpecialist');
  const nextBtn = document.getElementById('nextSpecialist');
  
  if (!grid || !prevBtn || !nextBtn) return;

  let currentSlide = 0;
  const cards = grid.querySelectorAll('.specialist-card');
  const totalCards = cards.length;

  prevBtn.addEventListener('click', () => {
    currentSlide = (currentSlide - 1 + totalCards) % totalCards;
    updateCarousel();
  });

  nextBtn.addEventListener('click', () => {
    currentSlide = (currentSlide + 1) % totalCards;
    updateCarousel();
  });

  function updateCarousel() {
    cards.forEach((card, index) => {
      card.style.opacity = index === currentSlide ? '1' : '0.6';
      card.style.transform = index === currentSlide ? 'scale(1.02)' : 'scale(1)';
    });
  }
}

// ======= SMOOTH SCROLL =======
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// ======= CHATBOT FUNCTIONS =======
const chatWindow = document.getElementById('chatWindow');
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');

function toggleChat() {
  if (chatWindow) {
    chatWindow.classList.toggle('active');
    if (chatWindow.classList.contains('active') && chatInput) {
      setTimeout(() => chatInput.focus(), 300);
    }
  }
}

function quickAsk(text) {
  if (chatInput) {
    chatInput.value = text;
    handleChat();
  }
}

function handleChat() {
  if (!chatInput || !chatBody) return;
  
  const text = chatInput.value.trim();
  if (!text) return;
  
  addMessage(text, 'user');
  chatInput.value = '';
  
  // Show typing indicator
  const typingDiv = document.createElement('div');
  typingDiv.className = 'msg-bubble msg-bot';
  typingDiv.innerHTML = '<span style="opacity: 0.6;">Escribiendo...</span>';
  typingDiv.id = 'typingIndicator';
  chatBody.appendChild(typingDiv);
  chatBody.scrollTop = chatBody.scrollHeight;

  setTimeout(() => {
    const typing = document.getElementById('typingIndicator');
    if (typing) typing.remove();
    
    let response = getBotResponse(text);
    addMessage(response, 'bot');
  }, 1200);
}

function getBotResponse(text) {
  const t = text.toLowerCase();
  
  if (t.includes('cita') || t.includes('reserv') || t.includes('agendar') || t.includes('turno')) {
    return '¡Perfecto! Te ayudo a agendar una cita. 📅<br><br>Puedes usar nuestro <a href="/citas/agendar/" style="color: #0891b2; font-weight: 600;">sistema de reservas online</a> o llamar al (4) 4220228.';
  }
  
  if (t.includes('horario') || t.includes('hora')) {
    return '🕐 <strong>Horarios de atención:</strong><br>• Emergencias: 24/7<br>• Consultas: Lun-Vie 08:00-18:00<br>• Sábados: 08:00-12:00';
  }
  
  if (t.includes('cardio')) {
    return '❤️ La unidad de <strong>Cardiología</strong> cuenta con especialistas certificados. Atendemos de Lunes a Viernes. <a href="/citas/agendar/" style="color: #0891b2;">Agendar cita</a>';
  }
  
  if (t.includes('emergencia') || t.includes('urgencia')) {
    return '🚑 <strong>Emergencias:</strong> Servicio disponible las 24 horas, los 7 días de la semana. Dirección: Hospital Tiquipaya, Cochabamba.';
  }
  
  if (t.includes('ubicación') || t.includes('donde') || t.includes('dirección')) {
    return '📍 Estamos ubicados en <strong>Tiquipaya, Cochabamba, Bolivia</strong>. ¡Te esperamos!';
  }
  
  if (t.includes('telefono') || t.includes('llamar') || t.includes('contacto')) {
    return '📞 <strong>Contacto:</strong><br>• Teléfono: (4) 4220228<br>• Horario: Lun-Sab, 8am-6pm';
  }
  
  return 'Gracias por tu consulta. Para información más específica, te recomiendo <a href="/citas/agendar/" style="color: #0891b2;">agendar una cita</a> o llamar al (4) 4220228. ¿Hay algo más en lo que pueda ayudarte?';
}

function addMessage(text, type) {
  if (!chatBody) return;
  
  const div = document.createElement('div');
  div.className = `msg-bubble msg-${type}`;
  div.innerHTML = text;
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// ======= SCROLL ANIMATIONS =======
window.addEventListener('scroll', function() {
  const sections = document.querySelectorAll('section');
  
  sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top < window.innerHeight * 0.8) {
      section.style.opacity = '1';
      section.style.transform = 'translateY(0)';
    }
  });
});