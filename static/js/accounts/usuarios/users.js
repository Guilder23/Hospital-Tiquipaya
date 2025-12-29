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

    // === BUSCADOR Y FILTROS EN TIEMPO REAL ===
    const inputBuscar = document.getElementById('buscar-usuario');
    const filtroTipo = document.getElementById('filtro-tipo');
    const filtroEstado = document.getElementById('filtro-estado');
    const filtroFecha = document.getElementById('filtro-fecha');
    const tablaBody = document.querySelector('.table tbody');
    const todasLasFilas = Array.from(tablaBody.querySelectorAll('tr'));

    function filtrarTabla() {
        const textoBusqueda = normalize(inputBuscar.value);
        const tipoSeleccionado = normalize(filtroTipo.value);
        const estadoSeleccionado = filtroEstado.value.toLowerCase();
        const ordenFecha = filtroFecha ? filtroFecha.value : '';

        let filasVisibles = [];

        todasLasFilas.forEach(fila => {
            // Obtener datos de la fila
            const nombres = normalize(fila.getAttribute('data-nombres') || '');
            const apellidoPaterno = normalize(fila.getAttribute('data-apellido_paterno') || '');
            const apellidoMaterno = normalize(fila.getAttribute('data-apellido_materno') || '');
            const ci = normalize(fila.getAttribute('data-ci') || '');
            const rol = normalize(fila.getAttribute('data-rol') || '');
            const activo = fila.getAttribute('data-active') === 'true';

            // Concatenar nombre completo para búsqueda
            const nombreCompleto = `${nombres} ${apellidoPaterno} ${apellidoMaterno}`.trim();

            // Verificar coincidencia con texto de búsqueda
            const coincideBusqueda = !textoBusqueda || 
                nombreCompleto.includes(textoBusqueda) || 
                ci.includes(textoBusqueda);

            // Verificar coincidencia con filtro de tipo
            const coincideTipo = !tipoSeleccionado || rol.includes(tipoSeleccionado);

            // Verificar coincidencia con filtro de estado
            let coincideEstado = true;
            if (estadoSeleccionado === 'activo') {
                coincideEstado = activo;
            } else if (estadoSeleccionado === 'inactivo') {
                coincideEstado = !activo;
            }

            // Mostrar u ocultar fila
            if (coincideBusqueda && coincideTipo && coincideEstado) {
                fila.style.display = '';
                filasVisibles.push(fila);
            } else {
                fila.style.display = 'none';
            }
        });

        // Ordenar por fecha si se seleccionó
        if (ordenFecha && filasVisibles.length > 0) {
            filasVisibles.sort((a, b) => {
                const fechaA = new Date(a.getAttribute('data-fecha-registro') || '1900-01-01');
                const fechaB = new Date(b.getAttribute('data-fecha-registro') || '1900-01-01');
                
                if (ordenFecha === 'desc') {
                    return fechaB - fechaA; // Más recientes primero
                } else {
                    return fechaA - fechaB; // Más antiguos primero
                }
            });

            // Reordenar filas en el DOM
            filasVisibles.forEach(fila => {
                tablaBody.appendChild(fila);
            });
        }

        // Mostrar mensaje si no hay resultados
        const filaVacia = tablaBody.querySelector('.fila-sin-resultados');
        if (filasVisibles.length === 0 && todasLasFilas.length > 0) {
            if (!filaVacia) {
                const tr = document.createElement('tr');
                tr.className = 'fila-sin-resultados';
                tr.innerHTML = '<td colspan="10" style="text-align: center; padding: 20px; color: #64748b;">No se encontraron usuarios que coincidan con los criterios de búsqueda</td>';
                tablaBody.appendChild(tr);
            }
        } else if (filaVacia) {
            filaVacia.remove();
        }
    }

    // Eventos para búsqueda en tiempo real
    if (inputBuscar) {
        inputBuscar.addEventListener('input', filtrarTabla);
    }

    if (filtroTipo) {
        filtroTipo.addEventListener('change', filtrarTabla);
    }

    if (filtroEstado) {
        filtroEstado.addEventListener('change', filtrarTabla);
    }

    if (filtroFecha) {
        filtroFecha.addEventListener('change', filtrarTabla);
    }

    // === FIN BUSCADOR ===

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
