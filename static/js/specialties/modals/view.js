document.addEventListener("DOMContentLoaded", () => {
    const modalView = document.getElementById("modal-view");

    document.querySelectorAll(".btn-view").forEach(btn => {
        btn.addEventListener("click", () => {
            const tr = btn.closest("tr");

            document.getElementById("view-nombre").textContent = tr.dataset.nombre;
            document.getElementById("view-descripcion").textContent = tr.dataset.descripcion || "Sin descripción";

            modalView.setAttribute("aria-hidden", "false");
        });
    });

    // Cerrar con botón X y backdrop
    modalView.querySelectorAll("[data-close]").forEach(el => {
        el.addEventListener("click", () => {
            modalView.setAttribute("aria-hidden", "true");
        });
    });
});
