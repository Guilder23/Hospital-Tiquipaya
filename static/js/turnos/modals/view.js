document.addEventListener('DOMContentLoaded', function() {
    const mView = document.getElementById('modal-ver-turno');
    
    // Abrir modal
    const openModal = (m) => { 
        if (m) { 
            m.style.display = 'flex'; 
            m.setAttribute('aria-hidden', 'false'); 
        } 
    };

    // Cerrar modal (FALTABA)
    const closeModal = (m) => { 
        if (m) { 
            m.style.display = 'none'; 
            m.setAttribute('aria-hidden', 'true'); 
        }
    };

    const set = (idSel, val) => { 
        const el = document.getElementById(idSel); 
        if (el) el.textContent = val || ''; 
    };

    // Cerrar modal al tocar fondo oscuro o botón
    document.querySelectorAll('[data-close]').forEach(el =>
        el.addEventListener('click', () => closeModal(mView))
    );

    // Abrir modal al hacer clic en Ver
    document.querySelectorAll('.btn-view').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('data-id');
            const row = document.querySelector(`tr[data-id="${id}"]`);
            if (row) {
                set('view-nombre', row.getAttribute('data-nombre'));
                set('view-hora_ini', row.getAttribute('data-hora_ini'));
                set('view-hora_fin', row.getAttribute('data-hora_fin'));
                set('view-estado', row.getAttribute('data-estado'));const estadoRaw = row.getAttribute('data-estado');
                set('view-estado', estadoRaw === "True" ? "Activo" : "Inactivo");
                openModal(mView);
            }
        });
    });
});
