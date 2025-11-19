// abrir modal crear
document.getElementById("btn-open-create").addEventListener("click", () => {
    document.getElementById("modal-crear").classList.add("is-open");
});

// cerrar modal
document.querySelectorAll("[data-close]").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".modal").forEach(m => m.classList.remove("is-open"));
    });
});

// abrir modal editar
document.querySelectorAll(".btn-edit").forEach(btn => {
    btn.addEventListener("click", () => {
        const row = btn.closest("tr");

        document.querySelector("#modal-editar input[name='nombre']").value = row.dataset.nombre;
        document.querySelector("#modal-editar textarea[name='descripcion']").value = row.dataset.descripcion;

        document.getElementById("modal-editar").classList.add("is-open");

        document.getElementById("form-edit").action = `/especialidades/editar/${row.dataset.id}/`;
    });
});

document.querySelectorAll(".modal").forEach(modal => {
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("is-open");
        }
    });
});

// evitar que clic dentro del modal cierre el modal
document.querySelectorAll(".modal").forEach(modal => {
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("is-open");
        }
    });
});
