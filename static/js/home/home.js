// CONTADORES PARA ESTADÍSTICAS
document.addEventListener('DOMContentLoaded', function() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.animated) {
        animateCounter(entry.target);
        entry.target.dataset.animated = 'true';
      }
    });
  }, observerOptions);

  // Animar contadores cuando entren en vista
  document.querySelectorAll('.stat-card').forEach(card => {
    observer.observe(card);
  });

  // Agregar efecto de scroll suave a los testimonios
  addTestimonialScroll();
});

function animateCounter(card) {
  const numberElement = card.querySelector('.stat-number');
  const targetText = numberElement.textContent;
  let targetNumber = parseInt(targetText);
  
  // Extraer solo el número
  if (targetText.includes('K')) {
    targetNumber = parseInt(targetText) * 1000;
  }
  
  let currentNumber = 0;
  const increment = targetNumber / 30; // 30 frames de animación
  const duration = 800; // 800ms
  const startTime = Date.now();

  function updateNumber() {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    currentNumber = Math.floor(targetNumber * progress);
    
    if (targetText.includes('K')) {
      numberElement.textContent = Math.floor(currentNumber / 1000) + 'K+';
    } else if (targetText.includes('/7')) {
      numberElement.textContent = '24/7';
    } else {
      numberElement.textContent = currentNumber + '+';
    }
    
    if (progress < 1) {
      requestAnimationFrame(updateNumber);
    } else {
      numberElement.textContent = targetText;
    }
  }

  updateNumber();
}

// Efecto parallax en hero section
window.addEventListener('scroll', function() {
  const hero = document.querySelector('.hero');
  const scrollPosition = window.pageYOffset;
  
  if (hero) {
    hero.style.backgroundPosition = '0 ' + (scrollPosition * 0.5) + 'px';
  }
});

// Agregue interactividad a las tarjetas
document.querySelectorAll('.feature-card, .specialty-card, .testimonial-card').forEach(card => {
  card.addEventListener('mouseenter', function() {
    this.style.cursor = 'pointer';
  });
});

// Función para scroll en testimonios (futuro)
function addTestimonialScroll() {
  const testimonials = document.querySelectorAll('.testimonial-card');
  let currentIndex = 0;

  // Opcional: auto scroll cada 5 segundos
  setInterval(() => {
    testimonials.forEach((card, index) => {
      card.style.opacity = index === currentIndex ? '1' : '0.7';
    });
    currentIndex = (currentIndex + 1) % testimonials.length;
  }, 5000);
}