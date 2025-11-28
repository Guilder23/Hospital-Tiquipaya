document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("modal-crear-usuario");

    function openModal() {
        modal.setAttribute("aria-hidden", "false");
    }

    function closeModal() {
        modal.setAttribute("aria-hidden", "true");
    }

    document.querySelectorAll("[data-open='crear-usuario']").forEach(btn =>
        btn.addEventListener("click", openModal)
    );

    modal.querySelectorAll("[data-close]").forEach(btn =>
        btn.addEventListener("click", closeModal)
    );
});
