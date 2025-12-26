/* ======= HOME NAVBAR SCRIPTS ======= */
document.addEventListener('DOMContentLoaded', function() {
  initMobileMenu();
  initNavbarScroll();
  initSmoothScrollNav();
});

// Mobile menu toggle
function initMobileMenu() {
  const toggle = document.getElementById('navbarToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  
  if (!toggle || !mobileMenu) return;
  
  toggle.addEventListener('click', function() {
    mobileMenu.classList.toggle('active');
    
    // Toggle icon
    const icon = toggle.querySelector('i');
    if (icon) {
      if (mobileMenu.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
      } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    }
  });
  
  // Close menu when clicking a link
  const menuLinks = mobileMenu.querySelectorAll('.ht-nav-link');
  menuLinks.forEach(link => {
    link.addEventListener('click', function() {
      mobileMenu.classList.remove('active');
      const icon = toggle.querySelector('i');
      if (icon) {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    });
  });
  
  // Close menu when clicking outside
  document.addEventListener('click', function(e) {
    if (!toggle.contains(e.target) && !mobileMenu.contains(e.target)) {
      mobileMenu.classList.remove('active');
      const icon = toggle.querySelector('i');
      if (icon) {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
      }
    }
  });
}

// Navbar scroll effect
function initNavbarScroll() {
  const navbar = document.querySelector('.home-navbar');
  if (!navbar) return;
  
  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(255, 255, 255, 0.98)';
      navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)';
    } else {
      navbar.style.background = 'rgba(255, 255, 255, 0.9)';
      navbar.style.boxShadow = 'none';
    }
  });
}

// Smooth scroll for nav links
function initSmoothScrollNav() {
  const navLinks = document.querySelectorAll('.ht-nav-link[href^="#"]');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      
      if (target) {
        const navbarHeight = document.querySelector('.home-navbar')?.offsetHeight || 70;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
        
        // Update active state
        navLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
      }
    });
  });
  
  // Update active link on scroll
  window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navbarHeight = document.querySelector('.home-navbar')?.offsetHeight || 70;
    
    sections.forEach(section => {
      const sectionTop = section.offsetTop - navbarHeight - 100;
      const sectionBottom = sectionTop + section.offsetHeight;
      
      if (window.scrollY >= sectionTop && window.scrollY < sectionBottom) {
        const id = section.getAttribute('id');
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          }
        });
      }
    });
  });
}
