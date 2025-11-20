// Maneja la confirmación de bloqueo/desactivación con modal
document.addEventListener("DOMContentLoaded", () => {
  const modalBlock = document.getElementById("modal-confirm-block");
  const btnConfirmBlock = document.getElementById("btn-block-confirm"); // enlace o botón que realiza la acción
  const cancelBtns = modalBlock ? modalBlock.querySelectorAll(".btn-cancel-block, .btn-cancel-modal") : [];

  // Cuando se haga click en un botón de bloqueo de la tabla
  document.querySelectorAll(".btn-block").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const url = btn.dataset.url;
      // Si btnConfirmBlock es <a>, colocamos href; si es button, colocamos data-action
      if (!btnConfirmBlock) return;

      if (btnConfirmBlock.tagName.toLowerCase() === "a") {
        btnConfirmBlock.setAttribute("href", url || "#");
      } else {
        // botón: guardamos la url en dataset y el backend puede leerla en submit
        btnConfirmBlock.dataset.action = url || "";
      }

      // opcional: actualizar mensaje dentro del modal si tenemos un span/párrafo
      const msg = modalBlock.querySelector("#block-message");
      if (msg && btn.dataset.nombre) {
        msg.textContent = `¿Seguro que deseas desactivar "${btn.dataset.nombre}"?`;
      }

      modalBlock.classList.add("is-open");
    });
  });

  // Cancelar dentro del modal
  cancelBtns.forEach(cb => {
    cb.addEventListener("click", () => {
      if (modalBlock) modalBlock.classList.remove("is-open");
    });
  });

  // Cerrar al click fuera del panel
  if (modalBlock) {
    modalBlock.addEventListener("click", (e) => {
      if (e.target === modalBlock) modalBlock.classList.remove("is-open");
    });
  }

  // Si btnConfirmBlock es un botón que debe enviar fetch/post en vez de enlace:
  if (btnConfirmBlock && btnConfirmBlock.tagName.toLowerCase() !== "a") {
    btnConfirmBlock.addEventListener("click", (e) => {
      const actionUrl = btnConfirmBlock.dataset.action;
      if (!actionUrl) return;

      // Realiza la petición con fetch POST (CSRF necesario). Si prefieres usar enlace, ignora este bloque.
      // Ejemplo simple: redirigir a la URL
      window.location.href = actionUrl;
    });
  }
});
