// Maneja apertura del modal editar y envío de datos al formulario de edición
document.addEventListener("DOMContentLoaded", () => {
  // Selector del modal y del form
  const modalEdit = document.getElementById("modal-editar");
  const formEdit = document.getElementById("form-edit");

  // botón(s) para cerrar dentro del modal editar (por si usas diferentes nombres)
  const closeSelectors = [
    ".btn-close-edit",      // botón específico
    ".btn-cancel-modal",    // botón genérico cancelar
    ".btn-close"            // otro posible nombre
  ];

  // Añadir evento a cada botón de editar (cada fila)
  document.querySelectorAll(".btn-edit").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const row = e.target.closest("tr");
      if (!row) return;

      // Rellenar inputs si existen
      const nombreInput = modalEdit?.querySelector("input[name='nombre']");
      const descTextarea = modalEdit?.querySelector("textarea[name='descripcion']");
      const idInput = modalEdit?.querySelector("input[name='id']"); // opcional si usas un input para id

      if (nombreInput) nombreInput.value = row.dataset.nombre ?? "";
      if (descTextarea) descTextarea.value = row.dataset.descripcion ?? "";
      if (idInput) idInput.value = row.dataset.id ?? "";

      // establecer action del form (si existe)
      if (formEdit) {
        formEdit.action = `/especialidades/editar/${row.dataset.id}/`;
      }

      // abrir modal
      if (modalEdit) modalEdit.classList.add("is-open");
    });
  });

  // Cerrar modal al click en botones de cerrar dentro del modal editar
  closeSelectors.forEach(sel => {
    modalEdit?.querySelectorAll(sel)?.forEach(btn => {
      btn.addEventListener("click", () => {
        modalEdit.classList.remove("is-open");
      });
    });
  });

  // Cerrar modal al click fuera del panel
  if (modalEdit) {
    modalEdit.addEventListener("click", (e) => {
      if (e.target === modalEdit) modalEdit.classList.remove("is-open");
    });
  }
});
