document.addEventListener("DOMContentLoaded", () => {
    const btnOpenCreate = document.getElementById("btn-open-create");
    const modalCrear = document.getElementById("modal-create");

    // ========== VALIDACIONES EN TIEMPO REAL ==========
    const nombreInput = document.getElementById("crear-nombre");
    const descripcionTextarea = document.getElementById("crear-descripcion");

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

    if (btnOpenCreate && modalCrear) {
        btnOpenCreate.addEventListener("click", () => {
            modalCrear.setAttribute("aria-hidden", "false");
        });

        // Cerrar con botón X y backdrop
        modalCrear.querySelectorAll("[data-close]").forEach(el => {
            el.addEventListener("click", () => {
                modalCrear.setAttribute("aria-hidden", "true");
            });
        });
    }
});
