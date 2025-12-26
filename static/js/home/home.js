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