document.addEventListener("DOMContentLoaded", () => {
    console.log("✓ Script crear.js cargado");
    
    const modal = document.getElementById("modal-crear-usuario");
    if (!modal) {
        console.error("✗ Modal NO encontrado");
        return;
    }

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

    // Buscar elementos dentro del modal
    const form = modal.querySelector("form");
    const selectRol = form ? form.querySelector("#select-rol") : null;
    
    console.log("selectRol:", selectRol ? "✓ encontrado" : "✗ NO encontrado");

    // Función para mostrar/ocultar campos
    function actualizarCampos() {
        const rol = selectRol.value.toLowerCase().trim();
        console.log("Rol actual:", rol);

        // Obtener todos los campos condicionales
        const campos = {
            medico: form.querySelector("#campos-medico"),
            admision: form.querySelector("#campos-admision"),
            encargado: form.querySelector("#campos-encargado-admision"),
            ecografo: form.querySelector("#campos-ecografo")
        };

        // Ocultar todos
        Object.values(campos).forEach(campo => {
            if (campo) {
                campo.style.setProperty("display", "none", "important");
            }
        });

        // Mostrar según rol
        if (rol.includes("medico")) {
            console.log("→ Mostrando MEDICO");
            if (campos.medico) campos.medico.style.setProperty("display", "block", "important");
        } else if (rol.includes("admision") && !rol.includes("encargado")) {
            console.log("→ Mostrando ADMISION");
            if (campos.admision) campos.admision.style.setProperty("display", "block", "important");
        } else if (rol.includes("encargado") && rol.includes("admision")) {
            console.log("→ Mostrando ENCARGADO");
            if (campos.encargado) campos.encargado.style.setProperty("display", "block", "important");
        } else if (rol.includes("ecografo") || rol.includes("ecógrafo")) {
            console.log("→ Mostrando ECOGRAFO");
            if (campos.ecografo) campos.ecografo.style.setProperty("display", "block", "important");
        } else {
            console.log("→ Rol sin campos:", rol);
        }
    }

    if (selectRol) {
        // Ejecutar cuando se cambia el rol
        selectRol.addEventListener("change", actualizarCampos);
        
        // También al hacer blur/focus en el select
        selectRol.addEventListener("blur", actualizarCampos);
        
        // Y ejecutar una vez al cargar para que muestre si hay valor por defecto
        actualizarCampos();
    }
});




