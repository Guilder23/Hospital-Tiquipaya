document.addEventListener("DOMContentLoaded", () => {
    // Inicializar filtros
    initializeFiltros();

    const closeAllModals = () => {
        document.querySelectorAll(".modal").forEach(modal =>
            modal.classList.remove("is-open")
        );
    };

    document.querySelectorAll(".btn-modal-cancel").forEach(btn => {
        btn.addEventListener("click", closeAllModals);
    });

    document.querySelectorAll(".modal-overlay").forEach(overlay => {
        overlay.addEventListener("click", closeAllModals);
    });

    // -------- MODAL CREATE ----------
    const btnOpenCreate = document.getElementById("btn-open-create");
    const modalCreate = document.getElementById("modal-create");

    if (btnOpenCreate && modalCreate) {
        btnOpenCreate.addEventListener("click", () => {
            modalCreate.classList.add("is-open");
        });
    }

    // -------- MODAL EDIT ----------
    document.querySelectorAll(".btn-edit").forEach(btn => {
        btn.addEventListener("click", () => {
            const row = btn.closest("tr");

            document.querySelector("#modal-edit input[name='nombre']").value = row.dataset.nombre;
            document.querySelector("#modal-edit textarea[name='descripcion']").value = row.dataset.descripcion;

            document.getElementById("modal-edit").classList.add("is-open");

            document.getElementById("form-edit").action =
                `/especialidades/editar/${row.dataset.id}/`;
        });
    });

    // -------- CONFIRM BLOCK ----------
    const modalBlock = document.getElementById("modal-confirm-block");
    const btnConfirmBlock = document.getElementById("btn-block-confirm");

    document.querySelectorAll(".btn-block").forEach(btn => {
        btn.addEventListener("click", () => {
            btnConfirmBlock.href = btn.dataset.url;
            modalBlock.classList.add("is-open");
        });
    });
});

function initializeFiltros() {
    const inputBusqueda = document.getElementById('buscar-especialidad');
    const selectEstado = document.getElementById('filtro-estado');
    const selectOrdenFecha = document.getElementById('filtro-orden-fecha');
    const tabla = document.querySelector('.table tbody');
    
    if (!tabla) return;
    
    const filas = Array.from(tabla.getElementsByTagName('tr'));

    // Función para normalizar texto
    function normalize(text) {
        return text.normalize('NFD')
                   .replace(/[\u0300-\u036f]/g, '')
                   .toLowerCase()
                   .trim();
    }

    // Función principal de filtrado
    function filtrarTabla() {
        const textoBusqueda = normalize(inputBusqueda ? inputBusqueda.value : '');
        const estadoSeleccionado = selectEstado ? selectEstado.value : '';
        const ordenFecha = selectOrdenFecha ? selectOrdenFecha.value : '';

        let filasVisibles = filas.filter(fila => {
            if (fila.querySelector('td[colspan]')) return false;

            const nombre = normalize(fila.getAttribute('data-nombre') || '');
            const estado = fila.getAttribute('data-estado') || '';
            
            const coincideBusqueda = nombre.includes(textoBusqueda);
            const coincideEstado = !estadoSeleccionado || estado === estadoSeleccionado;
            
            return coincideBusqueda && coincideEstado;
        });

        if (ordenFecha) {
            filasVisibles.sort((a, b) => {
                const fechaA = new Date(a.getAttribute('data-creado_en'));
                const fechaB = new Date(b.getAttribute('data-creado_en'));
                return ordenFecha === 'desc' ? fechaB - fechaA : fechaA - fechaB;
            });
        }

        filas.forEach(fila => fila.style.display = 'none');
        filasVisibles.forEach(fila => {
            fila.style.display = '';
            if (ordenFecha) tabla.appendChild(fila);
        });
    }

    if (inputBusqueda) inputBusqueda.addEventListener('input', filtrarTabla);
    if (selectEstado) selectEstado.addEventListener('change', filtrarTabla);
    if (selectOrdenFecha) selectOrdenFecha.addEventListener('change', filtrarTabla);
}
