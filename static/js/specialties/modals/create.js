document.addEventListener("DOMContentLoaded", () => {
    const btnOpenCreate = document.getElementById("btn-open-create");
    const modalCrear = document.getElementById("modal-crear");

    btnOpenCreate.addEventListener("click", () => {
        modalCrear.classList.add("is-open");
    });
});
