document.addEventListener("DOMContentLoaded", () => {

    const closeAllModals = () => {
        document.querySelectorAll(".modal").forEach(modal =>
            modal.classList.remove("is-open")
        );
    };

    document.querySelectorAll(".btn-modal-cancel").forEach(btn => {
        btn.addEventListener("click", closeAllModals);
    });

    document.querySelectorAll(".modal-overlay").forEach(overlay => {
        overlay.addEventListener("click", closeAllModals);
    });

    // -------- MODAL CREATE ----------
    const btnOpenCreate = document.getElementById("btn-open-create");
    const modalCreate = document.getElementById("modal-create");

    if (btnOpenCreate && modalCreate) {
        btnOpenCreate.addEventListener("click", () => {
            modalCreate.classList.add("is-open");
        });
    }

    // -------- MODAL EDIT ----------
    document.querySelectorAll(".btn-edit").forEach(btn => {
        btn.addEventListener("click", () => {
            const row = btn.closest("tr");

            document.querySelector("#modal-edit input[name='nombre']").value = row.dataset.nombre;
            document.querySelector("#modal-edit textarea[name='descripcion']").value = row.dataset.descripcion;

            document.getElementById("modal-edit").classList.add("is-open");

            document.getElementById("form-edit").action =
                `/especialidades/editar/${row.dataset.id}/`;
        });
    });

    // -------- CONFIRM BLOCK ----------
    const modalBlock = document.getElementById("modal-confirm-block");
    const btnConfirmBlock = document.getElementById("btn-block-confirm");

    document.querySelectorAll(".btn-block").forEach(btn => {
        btn.addEventListener("click", () => {
            btnConfirmBlock.href = btn.dataset.url;
            modalBlock.classList.add("is-open");
        });
    });
});
