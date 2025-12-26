/* ======= HOME FOOTER SCRIPTS ======= */
document.addEventListener('DOMContentLoaded', function() {
  initFooterAnimations();
});

// Animate footer elements on scroll into view
function initFooterAnimations() {
  const footer = document.querySelector('.home-footer');
  if (!footer) return;
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('footer-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  
  const footerSections = footer.querySelectorAll('.footer-section');
  footerSections.forEach((section, index) => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = `all 0.5s ease ${index * 0.1}s`;
    observer.observe(section);
  });
}

// Add visible class styles via JS
const style = document.createElement('style');
style.textContent = `
  .footer-section.footer-visible,
  .home-footer .footer-section {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
`;
document.head.appendChild(style);
