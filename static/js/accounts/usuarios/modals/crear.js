document.addEventListener("DOMContentLoaded", () => {
    console.log("✓ Script crear.js cargado");
    
    const modal = document.getElementById("modal-crear-usuario");
    if (!modal) {
        console.error("✗ Modal NO encontrado");
        return;
    }

    // ========== VALIDACIONES EN TIEMPO REAL ==========
    const form = modal.querySelector("form");
    
    // Calcular fecha mínima (18 años atrás) y máxima (85 años atrás)
    function calcularFechaMaxima() {
        const hoy = new Date();
        hoy.setFullYear(hoy.getFullYear() - 18);
        return hoy.toISOString().split('T')[0];
    }
    
    function calcularFechaMinima() {
        const hoy = new Date();
        hoy.setFullYear(hoy.getFullYear() - 85);
        return hoy.toISOString().split('T')[0];
    }
    
    // Establecer fecha máxima y mínima en el input de fecha de nacimiento
    const fechaNacInput = form?.querySelector('[name="fecha_nacimiento"]');
    if (fechaNacInput) {
        fechaNacInput.setAttribute('max', calcularFechaMaxima());
        fechaNacInput.setAttribute('min', calcularFechaMinima());
    }
    
    // Validar campos de texto alfabéticos (nombres y apellidos) - máximo 30 caracteres
    const camposAlfabeticos = form?.querySelectorAll('[name="nombres"], [name="apellido_paterno"], [name="apellido_materno"]');
    camposAlfabeticos?.forEach(input => {
        input.addEventListener('input', function() {
            const regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g;
            if (regex.test(this.value)) {
                this.value = this.value.replace(regex, '');
            }
            if (this.value.length > 30) {
                this.value = this.value.slice(0, 30);
            }
        });
    });
    
    // Validar username (solo letras, números y guión bajo, máximo 2 números, máximo 30 caracteres)
    const usernameInput = form?.querySelector('[name="username"]');
    usernameInput?.addEventListener('input', function() {
        // Bloquear caracteres no permitidos
        const regex = /[^A-Za-z0-9_]/g;
        if (regex.test(this.value)) {
            this.value = this.value.replace(regex, '');
        }
        
        // Limitar a máximo 30 caracteres
        if (this.value.length > 30) {
            this.value = this.value.slice(0, 30);
        }
        
        // Contar números y limitar a máximo 2
        const numeros = this.value.match(/[0-9]/g) || [];
        if (numeros.length > 2) {
            // Eliminar números extras del final
            let contador = 0;
            this.value = this.value.split('').filter(char => {
                if (/[0-9]/.test(char)) {
                    contador++;
                    return contador <= 2;
                }
                return true;
            }).join('');
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
    
    // Validar dirección (alfanuméricos y caracteres permitidos, máximo 50 caracteres)
    const direccionInput = form?.querySelector('[name="direccion"]');
    direccionInput?.addEventListener('input', function() {
        const regex = /[^A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s#.,°-]/g;
        if (regex.test(this.value)) {
            this.value = this.value.replace(regex, '');
        }
        if (this.value.length > 50) {
            this.value = this.value.slice(0, 50);
        }
    });
    
    // Validar correo (máximo 50 caracteres)
    const correoInput = form?.querySelector('[name="correo"]');
    correoInput?.addEventListener('input', function() {
        if (this.value.length > 50) {
            this.value = this.value.slice(0, 50);
        }
    });
    
    // Validar contraseña (máximo 30 caracteres)
    const passwordInput = form?.querySelector('[name="password"]');
    passwordInput?.addEventListener('input', function() {
        if (this.value.length > 30) {
            this.value = this.value.slice(0, 30);
        }
    });
    
    // Validar matrícula (solo números, mínimo 4, máximo 15 dígitos)
    const matriculaInputs = form?.querySelectorAll('[name="nro_matricula"]');
    matriculaInputs?.forEach(input => {
        input.addEventListener('input', function() {
            const regex = /[^0-9]/g;
            if (regex.test(this.value)) {
                this.value = this.value.replace(regex, '');
            }
            if (this.value.length > 15) {
                this.value = this.value.slice(0, 15);
            }
        });
    });
    
    // Validar consultorio y ventanilla (solo números, máximo 2 dígitos)
    const consultoriosInputs = form?.querySelectorAll('[name="consultorio"], [name="ventanilla"]');
    consultoriosInputs?.forEach(input => {
        input.addEventListener('input', function() {
            const regex = /[^0-9]/g;
            if (regex.test(this.value)) {
                this.value = this.value.replace(regex, '');
            }
            if (this.value.length > 2) {
                this.value = this.value.slice(0, 2);
            }
        });
    });
    
    // Botón para mostrar/ocultar contraseña
    const togglePassword = document.getElementById('toggle-password');
    const passwordInputToggle = document.getElementById('password-input');
    if (togglePassword && passwordInputToggle) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInputToggle.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInputToggle.setAttribute('type', type);
            const eyeIcon = document.getElementById('eye-icon');
            eyeIcon.textContent = type === 'password' ? 'Ver' : 'Ocultar';
        });
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




