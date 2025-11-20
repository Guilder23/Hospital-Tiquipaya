document.addEventListener("DOMContentLoaded", () => {

    // ============================
    //   CERRAR TODOS LOS MODALS
    // ============================
    const closeAllModals = () => {
        document.querySelectorAll(".modal").forEach(modal =>
            modal.classList.remove("is-open")
        );
    };

    // Botones con clase .btn-cancel-modal (para cerrar)
    document.querySelectorAll(".btn-cancel-modal").forEach(btn => {
        btn.addEventListener("click", closeAllModals);
    });

    // Cerrar al hacer click fuera del contenido
    document.querySelectorAll(".modal").forEach(modal => {
        modal.addEventListener("click", e => {
            if (e.target === modal) modal.classList.remove("is-open");
        });
    });


    // =======================
    //  MODAL EDITAR
    // =======================
    document.querySelectorAll(".btn-edit").forEach(btn => {
        btn.addEventListener("click", () => {
            const row = btn.closest("tr");

            document.querySelector("#modal-editar input[name='nombre']").value = row.dataset.nombre;
            document.querySelector("#modal-editar textarea[name='descripcion']").value = row.dataset.descripcion;

            document.getElementById("modal-editar").classList.add("is-open");

            document.getElementById("form-edit").action =
                `/especialidades/editar/${row.dataset.id}/`;
        });
    });


    // =======================
    //  MODAL BLOQUEO
    // =======================
    const modalBlock = document.getElementById("modal-confirm-block");
    const btnConfirmBlock = document.getElementById("btn-block-confirm");

    document.querySelectorAll(".btn-block").forEach(btn => {
        btn.addEventListener("click", () => {
            btnConfirmBlock.href = btn.dataset.url;
            modalBlock.classList.add("is-open");
        });
    });
});
