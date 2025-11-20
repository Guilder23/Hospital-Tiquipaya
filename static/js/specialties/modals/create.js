document.addEventListener("DOMContentLoaded", () => {
    const btnOpenCreate = document.getElementById("btn-open-create");
    const modalCrear = document.getElementById("modal-crear");

    if (btnOpenCreate && modalCrear) {
        btnOpenCreate.addEventListener("click", () => {
            modalCrear.classList.add("is-open");
        });
    }
});
