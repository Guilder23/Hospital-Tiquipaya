// Maneja apertura del modal editar y envío de datos al formulario de edición
document.addEventListener("DOMContentLoaded", () => {
  const modalEdit = document.getElementById("modal-edit");
  const formEdit = document.getElementById("form-edit");

  // ========== VALIDACIONES EN TIEMPO REAL ==========
  const nombreInput = document.getElementById("editar-nombre");
  const descripcionTextarea = document.getElementById("editar-descripcion");

  // Validar nombre: solo caracteres alfabéticos (no números ni símbolos extraños)
  if (nombreInput) {
    nombreInput.addEventListener('input', function() {
      const regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g;
      if (regex.test(this.value)) {
        this.value = this.value.replace(regex, '');
      }
    });
  }

  // Validar descripción: caracteres alfanuméricos y puntuación básica
  if (descripcionTextarea) {
    descripcionTextarea.addEventListener('input', function() {
      const regex = /[^A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s.,;:¿?¡!()-]/g;
      if (regex.test(this.value)) {
        this.value = this.value.replace(regex, '');
      }
    });
  }

  // Añadir evento a cada botón de editar (cada fila)
  document.querySelectorAll(".btn-edit").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const row = e.target.closest("tr");
      if (!row) return;

      // Rellenar inputs si existen
      const nombreInput = document.getElementById("editar-nombre");
      const descTextarea = document.getElementById("editar-descripcion");

      if (nombreInput) nombreInput.value = row.dataset.nombre ?? "";
      if (descTextarea) descTextarea.value = row.dataset.descripcion ?? "";

      // establecer action del form (si existe)
      if (formEdit) {
        formEdit.action = `/especialidades/editar/${row.dataset.id}/`;
      }

      // abrir modal
      if (modalEdit) modalEdit.setAttribute("aria-hidden", "false");
    });
  });

  // Cerrar modal con botón X y backdrop
  if (modalEdit) {
    modalEdit.querySelectorAll("[data-close]").forEach(el => {
      el.addEventListener("click", () => {
        modalEdit.setAttribute("aria-hidden", "true");
      });
    });
  }
});
