document.addEventListener("DOMContentLoaded", () => {
    console.log("✓ Script crear.js cargado");
    
    const modal = document.getElementById("modal-crear-usuario");
    if (!modal) {
        console.error("✗ Modal NO encontrado");
        return;
    }

    // ========== VALIDACIONES EN TIEMPO REAL ==========
    const form = modal.querySelector("form");
    
    // Calcular fecha mínima (18 años atrás)
    function calcularFechaMaxima() {
        const hoy = new Date();
        hoy.setFullYear(hoy.getFullYear() - 18);
        return hoy.toISOString().split('T')[0];
    }
    
    // Establecer fecha máxima en el input de fecha de nacimiento
    const fechaNacInput = form?.querySelector('[name="fecha_nacimiento"]');
    if (fechaNacInput) {
        fechaNacInput.setAttribute('max', calcularFechaMaxima());
    }
    
    // Validar campos de texto alfabéticos (nombres y apellidos)
    const camposAlfabeticos = form?.querySelectorAll('[name="nombres"], [name="apellido_paterno"], [name="apellido_materno"]');
    camposAlfabeticos?.forEach(input => {
        input.addEventListener('input', function() {
            const regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g;
            if (regex.test(this.value)) {
                this.value = this.value.replace(regex, '');
            }
        });
    });
    
    // Validar username (solo letras, números y guión bajo)
    const usernameInput = form?.querySelector('[name="username"]');
    usernameInput?.addEventListener('input', function() {
        //[^A-Za-z0-9_]/
        const regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g;
        if (regex.test(this.value)) {
            this.value = this.value.replace(regex, '');
        }
    });
    
    // Validar CI (solo números, 7-8 dígitos)
    const ciInput = form?.querySelector('[name="ci"]');
    ciInput?.addEventListener('input', function() {
        const regex = /[^0-9]/g;
        if (regex.test(this.value)) {
            this.value = this.value.replace(regex, '');
        }
        if (this.value.length > 8) {
            this.value = this.value.slice(0, 8);
        }
    });
    
    // Validar complemento CI (alfanumérico, 2-4 caracteres)
    const complementoInput = form?.querySelector('[name="complemento_ci"]');
    complementoInput?.addEventListener('input', function() {
        const regex = /[^A-Za-z0-9]/g;
        if (regex.test(this.value)) {
            this.value = this.value.replace(regex, '');
        }
        if (this.value.length > 4) {
            this.value = this.value.slice(0, 4);
        }
    });
    
    // Validar teléfonos (solo números, 8 dígitos)
    const telefonosInputs = form?.querySelectorAll('[name="telefono"], [name="celular"]');
    telefonosInputs?.forEach(input => {
        input.addEventListener('input', function() {
            const regex = /[^0-9]/g;
            if (regex.test(this.value)) {
                this.value = this.value.replace(regex, '');
            }
            if (this.value.length > 8) {
                this.value = this.value.slice(0, 8);
            }
        });
    });
    
    // Validar dirección (alfanuméricos y caracteres permitidos)
    const direccionInput = form?.querySelector('[name="direccion"]');
    direccionInput?.addEventListener('input', function() {
        const regex = /[^A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s#.,°-]/g;
        if (regex.test(this.value)) {
            this.value = this.value.replace(regex, '');
        }
    });
    
    // Validar matrícula (alfanumérico)
    const matriculaInputs = form?.querySelectorAll('[name="nro_matricula"]');
    matriculaInputs?.forEach(input => {
        input.addEventListener('input', function() {
            const regex = /[^A-Za-z0-9-]/g;
            if (regex.test(this.value)) {
                this.value = this.value.replace(regex, '');
            }
        });
    });

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

    // Buscar elementos para campos condicionales
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




