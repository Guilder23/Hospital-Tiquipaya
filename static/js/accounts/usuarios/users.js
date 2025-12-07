document.addEventListener('DOMContentLoaded', function () {

     window.__modals = window.__modals || {};

    const normalize = function(str){
        if (!str) return '';
        return str
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .trim();
    };

    const selectRol = document.getElementById('select-rol');

    // Mostrar campos según el rol en el modal CREAR
    function toggleCamposCondicionales() {
        if (!selectRol) return;

        const rolSeleccionado = selectRol.options[selectRol.selectedIndex].text.trim();
        const rolNorm = normalize(rolSeleccionado);

        document.querySelectorAll('.campos-condicionales').forEach(bloque => {
            bloque.style.display = 'none';
            bloque.querySelectorAll('[required]').forEach(inp => inp.removeAttribute('required'));
        });

        if (rolNorm.includes('medico')) {
            const medico = document.getElementById('campos-medico');
            medico.style.display = 'block';
            medico.querySelector('select[name="especialidad"]').setAttribute('required', 'true');
        } else if ((rolNorm.includes('admision') && !rolNorm.includes('encargado')) || rolNorm.includes('recepcionista')) {
            const adm = document.getElementById('campos-admision');
            adm.style.display = 'block';
            adm.querySelector('input[name="ventanilla"]').setAttribute('required', 'true');
        } else if (rolNorm.includes('encargado') && rolNorm.includes('admision')) {
            const enc = document.getElementById('campos-encargado-admision');
            enc.style.display = 'block';
            enc.querySelector('input[name="ventanilla"]').setAttribute('required', 'true');
        }
    }

    if (selectRol) {
        toggleCamposCondicionales();
        selectRol.addEventListener('change', toggleCamposCondicionales);
    }

    // MODALES
    const modalCreate = document.getElementById('modal-crear-usuario');
    const modalEdit   = document.getElementById('modal-editar-usuario');
    const modalView   = document.getElementById('modal-ver-usuario');
    const modalDeshabilitar   = document.getElementById('modal-desactivar-usuario');

    function open(modal) {
        if (!modal) return;
        modal.setAttribute('aria-hidden', 'false');
        modal.classList.add('active', 'show');
    }

    function close(modal) {
        if (!modal) return;

        if (modal.contains(document.activeElement)) {
            document.activeElement.blur();
        }

        modal.setAttribute('aria-hidden', 'true');
        modal.classList.remove('active', 'show');
    }

    document.querySelectorAll('[data-close]').forEach(el =>
        el.addEventListener('click', () => {
            [modalCreate, modalEdit, modalView, modalDeshabilitar].forEach(m => m && close(m));
        })
    );

    const btnOpenCreate = document.getElementById('btn-open-create');
    if (btnOpenCreate) {
        btnOpenCreate.addEventListener('click', () => open(modalCreate));
    }

    // Exponer funciones a nivel global para los otros archivos
    window.__modals.open = open;
    window.__modals.close = close;
});
