document.addEventListener("DOMContentLoaded", () => {
    const modalView = document.getElementById("modal-view");
    const closeBtn = modalView.querySelector(".btn-close-view");

    document.querySelectorAll(".btn-view").forEach(btn => {
        btn.addEventListener("click", () => {
            const tr = btn.closest("tr");

            document.getElementById("view-nombre").textContent = tr.dataset.nombre;
            document.getElementById("view-descripcion").textContent = tr.dataset.descripcion;

            modalView.classList.add("is-open");
        });
    });

    closeBtn.addEventListener("click", () => modalView.classList.remove("is-open"));
});
