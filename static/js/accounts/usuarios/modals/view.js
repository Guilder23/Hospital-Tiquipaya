document.addEventListener('DOMContentLoaded', () => {
    const modalView = document.getElementById('modal-ver-usuario');

    const { open, close } = window.__modals;

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => close(modalView));
    });

    document.querySelectorAll('.btn-view').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.dataset.id;
            const row = document.querySelector(`tr[data-id="${id}"]`);
            if(!row) return;

            // Campos generales
            const campos = ['username','nombres','apellido_paterno','apellido_materno','email','ci','complemento','expedido','nacimiento','sexo','telefono','celular','direccion'];
            campos.forEach(c => {
                const el = document.getElementById('v-' + c.replace('_','-'));
                if(el) el.textContent = row.dataset[c] || '';
            });

            // Rol
            const rol = row.dataset.rol || "Sin rol";
            const elRol = document.getElementById('v-rol');
            if(elRol) elRol.textContent = rol;

            // Ocultar secciones
            ['v-medico','v-admision','v-encargado'].forEach(id => {
                const el = document.getElementById(id);
                if(el) el.style.display = 'none';
            });

            // Mostrar secciones según rol
            if(rol === "Medico" || rol === "Médico"){
                const grupo = document.getElementById('v-medico');
                if(grupo) grupo.style.display='block';
                ['especialidad','matricula','consultorio','turnos','dias'].forEach(c => {
                    const el = document.getElementById('v-'+c);
                    if(el) el.textContent = row.dataset[c] || '';
                });
            } else if(rol === "Admision" || rol === "Admisión"){
                const grupo = document.getElementById('v-admision');
                if(grupo) grupo.style.display='block';
                ['ventanilla','turnosadm'].forEach(c => {
                    const el = document.getElementById('v-' + c.replace(/([A-Z])/g,'-$1').toLowerCase());
                    if(el) el.textContent = row.dataset[c] || '';
                });
            } else if(rol === "Encargado" || rol === "Encargado de Admisión"){
                const grupo = document.getElementById('v-encargado');
                if(grupo) grupo.style.display='block';
                ['ventanillaenc','turnosenc'].forEach(c => {
                    const el = document.getElementById('v-' + c.replace(/([A-Z])/g,'-$1').toLowerCase());
                    if(el) el.textContent = row.dataset[c] || '';
                });
            }

            open(modalView);
        });
    });
});