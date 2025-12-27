document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal-eliminar-tipo');
  const form = document.getElementById('form-delete-tipo');
  const closeButtons = modal?.querySelectorAll('[data-close]');
  const deleteButtons = document.querySelectorAll('.btn-delete');
  const btnConfirmar = document.getElementById('btn-confirmar-eliminar');
  const usuariosWarning = document.getElementById('delete-usuarios-warning');
  const usuariosCount = document.getElementById('delete-usuarios-count');
  const warningText = document.getElementById('delete-warning-text');
  
  // Variable de estado para controlar si se puede eliminar
  let puedeEliminar = false;
  
  async function verificarUsuarios(id) {
    try {
      const response = await fetch(`/accounts/tipos/${id}/verificar/`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error verificando usuarios:', error);
      // En caso de error, NO permitir eliminar por seguridad
      return { puede_eliminar: false, usuarios_count: -1 };
    }
  }
  
  async function openModal(id, nombre) {
    if (!modal || !form) return;
    
    // Deshabilitar botón por defecto mientras se verifica
    puedeEliminar = false;
    if (btnConfirmar) {
      btnConfirmar.disabled = true;
      btnConfirmar.textContent = 'Verificando...';
      btnConfirmar.classList.add('btn-disabled');
    }
    if (usuariosWarning) usuariosWarning.style.display = 'none';
    if (warningText) warningText.style.display = 'none';
    
    form.setAttribute('action', `/accounts/tipos/${id}/eliminar/`);
    
    const textElement = document.getElementById('delete-tipo-text');
    if (textElement) {
      textElement.textContent = `¿Confirmas eliminar "${nombre}"?`;
    }
    
    // Mostrar modal inmediatamente
    modal.setAttribute('aria-hidden', 'false');
    
    // Verificar usuarios
    const verificacion = await verificarUsuarios(id);
    
    if (verificacion.usuarios_count > 0 || verificacion.usuarios_count === -1) {
      // Hay usuarios con este rol o hubo error - NO permitir eliminar
      puedeEliminar = false;
      if (usuariosWarning) {
        usuariosWarning.style.display = 'flex';
        if (verificacion.usuarios_count === -1) {
          usuariosCount.textContent = 'Error al verificar. No se puede eliminar por seguridad.';
        } else {
          usuariosCount.textContent = `No se puede eliminar. Hay ${verificacion.usuarios_count} usuario(s) con este rol asignado.`;
        }
      }
      if (warningText) {
        warningText.style.display = 'none';
      }
      if (btnConfirmar) {
        btnConfirmar.disabled = true;
        btnConfirmar.textContent = 'No disponible';
        btnConfirmar.classList.add('btn-disabled');
      }
    } else {
      // No hay usuarios - permitir eliminar
      puedeEliminar = true;
      if (usuariosWarning) {
        usuariosWarning.style.display = 'none';
      }
      if (warningText) {
        warningText.style.display = 'block';
      }
      if (btnConfirmar) {
        btnConfirmar.disabled = false;
        btnConfirmar.textContent = 'Eliminar';
        btnConfirmar.classList.remove('btn-disabled');
      }
      setTimeout(() => btnConfirmar?.focus(), 100);
    }
  }
  
  function closeModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'true');
    
    // Reset estado del modal
    puedeEliminar = false;
    if (usuariosWarning) usuariosWarning.style.display = 'none';
    if (warningText) warningText.style.display = 'block';
    if (btnConfirmar) {
      btnConfirmar.disabled = true;
      btnConfirmar.textContent = 'Eliminar';
      btnConfirmar.classList.remove('btn-disabled');
    }
  }
  
  // Prevenir envío si no se puede eliminar
  form?.addEventListener('submit', function(e) {
    if (!puedeEliminar) {
      e.preventDefault();
      e.stopPropagation();
      alert('No se puede eliminar este tipo de usuario porque tiene usuarios asignados.');
      return false;
    }
  });
  
  // Event listeners para botones eliminar
  deleteButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const id = this.getAttribute('data-id');
      const nombre = this.getAttribute('data-nombre');
      openModal(id, nombre);
    });
  });
  
  // Cerrar modal
  closeButtons?.forEach(btn => {
    btn.addEventListener('click', closeModal);
  });
  
  // Cerrar al presionar ESC
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal?.getAttribute('aria-hidden') === 'false') {
      closeModal();
    }
  });
  
  // Cerrar al hacer click en el backdrop
  const backdrop = modal?.querySelector('.modal-backdrop');
  backdrop?.addEventListener('click', closeModal);
});
