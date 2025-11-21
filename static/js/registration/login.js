document.addEventListener('DOMContentLoaded', function() {
  var overlay = document.getElementById('loginModalOverlay');
  function open() { if (!overlay) return; overlay.classList.add('active'); overlay.style.display = 'flex'; document.body.style.overflow = 'hidden'; }
  function close() { if (!overlay) return; overlay.classList.remove('active'); overlay.style.display = 'none'; document.body.style.overflow = 'auto'; }
  window.toggleLoginModal = function() { if (!overlay) return; if (overlay.classList.contains('active')) { close(); } else { open(); } };
  window.switchToRegisterModal = function() { close(); setTimeout(function(){ var ro = document.getElementById('registerModalOverlay'); if (ro) { ro.classList.add('active'); ro.style.display = 'flex'; document.body.style.overflow = 'hidden'; } }, 300); };
  if (overlay) { overlay.addEventListener('click', function(e){ if (e.target === overlay) { close(); } }); }
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') { if (overlay && overlay.classList.contains('active')) { close(); } } });
  var buttons = document.querySelectorAll('.btn');
  buttons.forEach(function(btn){ btn.addEventListener('mouseenter', function(){ this.style.transform = 'translateY(-2px)'; }); btn.addEventListener('mouseleave', function(){ this.style.transform = 'translateY(0)'; }); });
  var form = overlay ? overlay.querySelector('form.auth-form') : null;
  if (form) {
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var username = form.querySelector('input[name="username"]');
      var password = form.querySelector('input[name="password"]');
      var errorBox = document.getElementById('login-error');
      var isValid = true;
      if (!username || !username.value.trim()) { showError(username, 'El usuario es requerido'); isValid = false; } else { clearError(username); }
      if (!password || !password.value) { showError(password, 'La contraseña es requerida'); isValid = false; }
      else if (password.value.length < 6) { showError(password, 'La contraseña debe tener al menos 6 caracteres'); isValid = false; }
      else { clearError(password); }
      if (!isValid) { return; }
      var fd = new FormData(form);
      fetch(form.getAttribute('action'), { method: 'POST', body: fd, credentials: 'same-origin' })
        .then(function(res){
          if (res.redirected) {
            try{ localStorage.setItem('toast_message', 'Sesión iniciada correctamente'); localStorage.setItem('toast_type', 'success'); }catch(e){}
            close();
            setTimeout(function(){ window.location.href = res.url || '/'; }, 1000);
            return null;
          }
          return res.text();
        })
        .then(function(text){
          if (text === null) return;
          if (errorBox) { errorBox.textContent = 'Usuario o contraseña incorrectos'; errorBox.style.display = 'block'; }
        })
        .catch(function(){ if (errorBox) { errorBox.textContent = 'Error de conexión'; errorBox.style.display = 'block'; } });
    });
  }
  function showError(input, message) { if (!input) return; var existingError = input.parentElement.querySelector('.form-error'); if (existingError) existingError.remove(); var error = document.createElement('span'); error.className = 'form-error'; error.textContent = message; input.parentElement.appendChild(error); input.style.borderColor = '#ff6b6b'; }
  function clearError(input) { if (!input) return; var error = input.parentElement.querySelector('.form-error'); if (error) error.remove(); input.style.borderColor = '#e0e0e0'; }
});