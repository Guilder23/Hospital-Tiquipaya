// Maneja la confirmación de bloqueo/desactivación con modal
document.addEventListener("DOMContentLoaded", () => {
  const modalBlock = document.getElementById("modal-confirm-block");
  const btnConfirmBlock = document.getElementById("btn-block-confirm");

  // Cuando se haga click en un botón de bloqueo de la tabla
  document.querySelectorAll(".btn-delete").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const url = btn.dataset.url;
      if (!btnConfirmBlock) return;

      btnConfirmBlock.setAttribute("href", url || "#");

      // opcional: actualizar mensaje dentro del modal
      const msg = modalBlock.querySelector("#block-message");
      const nombre = btn.closest("tr")?.dataset.nombre;
      if (msg && nombre) {
        msg.textContent = `¿Confirmas desactivar "${nombre}"?`;
      }

      modalBlock.setAttribute("aria-hidden", "false");
    });
  });

  // Cerrar modal con botón X y backdrop
  if (modalBlock) {
    modalBlock.querySelectorAll("[data-close]").forEach(el => {
      el.addEventListener("click", () => {
        modalBlock.setAttribute("aria-hidden", "true");
      });
    });
  }
});
