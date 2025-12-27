document.addEventListener("DOMContentLoaded", () => {
    const btnOpenCreate = document.getElementById("btn-open-create");
    const modalCrear = document.getElementById("modal-create");

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
