document.addEventListener('DOMContentLoaded', function () {
    const ROL_MEDICO = "Medico";
    const ROL_ADMISION = "Admision";
    const ROL_ENCARGADO = "Encargado de Admisión";

    const selectRol = document.getElementById('select-rol');

    function toggleCamposCondicionales() {
        if (!selectRol) return;

        const rolSeleccionado = selectRol.options[selectRol.selectedIndex].text.trim();

        document.querySelectorAll('.campos-condicionales').forEach(bloque => {
            bloque.style.display = 'none';
            bloque.querySelectorAll('[required]').forEach(inp => inp.removeAttribute('required'));
        });

        if (rolSeleccionado === ROL_MEDICO) {
            const medico = document.getElementById('campos-medico');
            medico.style.display = 'block';
            medico.querySelector('select[name="especialidad"]').setAttribute('required', 'true');
        } else if (rolSeleccionado === ROL_ADMISION) {
            document.getElementById('campos-admision').style.display = 'block';
        } else if (rolSeleccionado === ROL_ENCARGADO) {
            document.getElementById('campos-encargado-admision').style.display = 'block';
        }
    }

    if (selectRol) {
        toggleCamposCondicionales();
        selectRol.addEventListener('change', toggleCamposCondicionales);
    }

    const modalCreate = document.getElementById('modal-crear-usuario');
    const modalEdit = document.getElementById('modal-editar-usuario');
    const modalDelete = document.getElementById('modal-eliminar-usuario');
    const modalView = document.getElementById('modal-ver-usuario');
    const btnOpenCreate = document.getElementById('btn-open-create');

    function open(modal) {
        modal.setAttribute('aria-hidden', 'false');
    }
    function close(modal) {
        modal.setAttribute('aria-hidden', 'true');
        if (modal === modalCreate && selectRol) {
            selectRol.value = '';
            toggleCamposCondicionales();
        }
    }

    document.querySelectorAll('[data-close]').forEach(el => el.addEventListener('click', () => {
        [modalCreate, modalEdit, modalDelete, modalView].forEach(m => m && close(m));
    }));

    if (btnOpenCreate) btnOpenCreate.addEventListener('click', () => open(modalCreate));

    // Editar Usuario
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const row = document.querySelector(`tr[data-id="${id}"]`);
            const form = document.getElementById('form-edit');

            form.setAttribute('action', `/accounts/usuarios/${id}/editar/`);
            form.querySelector('[name="username"]').value = row.getAttribute('data-username') || '';
            form.querySelector('[name="first_name"]').value = row.getAttribute('data-first_name') || '';
            form.querySelector('[name="last_name"]').value = row.getAttribute('data-last_name') || '';
            form.querySelector('[name="email"]').value = row.getAttribute('data-email') || '';
            const activeSel = form.querySelector('[name="is_active"]');
            if (activeSel) activeSel.value = row.getAttribute('data-active') === 'True' ? 'True' : 'False';
            const tipoSel = form.querySelector('[name="tipo"]');
            if (tipoSel) tipoSel.value = row.getAttribute('data-tipo_id') || '';
            open(modalEdit);
        });
    });

    // Eliminar Usuario
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const username = btn.getAttribute('data-username');
            const form = document.getElementById('form-delete');

            form.setAttribute('action', `/accounts/usuarios/${id}/eliminar/`);
            const txt = document.getElementById('delete-text');
            if (txt) txt.textContent = `¿Confirmas eliminar "${username}"?`;
            open(modalDelete);
        });
    });

    // Ver Usuario
    document.querySelectorAll('.btn-view').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const row = document.querySelector(`tr[data-id="${id}"]`);

            document.getElementById('view-username').textContent = row.getAttribute('data-username') || '';
            document.getElementById('view-name').textContent = (row.getAttribute('data-first_name') || '') + ' ' + (row.getAttribute('data-last_name') || '');
            document.getElementById('view-email').textContent = row.getAttribute('data-email') || '';
            document.getElementById('view-active').textContent = row.getAttribute('data-active') === 'True' ? 'Sí' : 'No';
            document.getElementById('view-rol').textContent = row.getAttribute('data-tipo_nombre') || 'Sin rol';

            open(modalView);
        });
    });
});
