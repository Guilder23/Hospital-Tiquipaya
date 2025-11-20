document.addEventListener('DOMContentLoaded', function() {
  var overlay = document.getElementById('registerModalOverlay');
  function open() { if (!overlay) return; overlay.classList.add('active'); overlay.style.display = 'flex'; document.body.style.overflow = 'hidden'; }
  function close() { if (!overlay) return; overlay.classList.remove('active'); overlay.style.display = 'none'; document.body.style.overflow = 'auto'; }
  window.toggleRegisterModal = function() { if (!overlay) return; if (overlay.classList.contains('active')) { close(); } else { open(); } };
  window.switchToLoginModal = function() { close(); setTimeout(function(){ var lo = document.getElementById('loginModalOverlay'); if (lo) { lo.classList.add('active'); lo.style.display = 'flex'; document.body.style.overflow = 'hidden'; } }, 300); };
  if (overlay) { overlay.addEventListener('click', function(e){ if (e.target === overlay) { close(); } }); }
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') { if (overlay && overlay.classList.contains('active')) { close(); } } });
  var buttons = document.querySelectorAll('.btn');
  buttons.forEach(function(btn){ btn.addEventListener('mouseenter', function(){ this.style.transform = 'translateY(-2px)'; }); btn.addEventListener('mouseleave', function(){ this.style.transform = 'translateY(0)'; }); });
  var form = overlay ? overlay.querySelector('form.auth-form') : null;
  if (form) {
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var fields = form.querySelectorAll('input, select, textarea');
      var errorBox = document.getElementById('register-error');
      var isValid = true;
      fields.forEach(function(field){
        if (field.hasAttribute('required') && !field.value.trim()) { showError(field, 'Este campo es requerido'); isValid = false; }
        else if (field.type === 'email' && field.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value)) { showError(field, 'Email inválido'); isValid = false; }
        else if (field.name === 'password1' && field.value && field.value.length < 6) { showError(field, 'Mínimo 6 caracteres'); isValid = false; }
        else if (field.name === 'password2') { var p1 = form.querySelector('input[name="password1"]'); if (p1 && field.value !== p1.value) { showError(field, 'Las contraseñas no coinciden'); isValid = false; } else { clearError(field); } }
        else { clearError(field); }
      });
      if (!isValid) { return; }
      var fd = new FormData(form);
      fetch(form.getAttribute('action'), { method: 'POST', body: fd, credentials: 'same-origin' })
        .then(function(res){
          if (res.redirected) {
            try{ localStorage.setItem('toast_message', 'Registro completado'); localStorage.setItem('toast_type', 'success'); }catch(e){}
            close();
            setTimeout(function(){ window.location.href = res.url || '/'; }, 1000);
            return null;
          }
          return res.text();
        })
        .then(function(text){
          if (text === null) return;
          if (errorBox) { errorBox.textContent = 'No se pudo registrar. Revisa los campos.'; errorBox.style.display = 'block'; }
        })
        .catch(function(){ if (errorBox) { errorBox.textContent = 'Error de conexión'; errorBox.style.display = 'block'; } });
    });
  }
  function showError(input, message) { if (!input) return; var existingError = input.parentElement.querySelector('.form-error'); if (existingError) existingError.remove(); var error = document.createElement('span'); error.className = 'form-error'; error.textContent = message; input.parentElement.appendChild(error); input.style.borderColor = '#ff6b6b'; }
  function clearError(input) { if (!input) return; var error = input.parentElement.querySelector('.form-error'); if (error) error.remove(); input.style.borderColor = '#e0e0e0'; }
});