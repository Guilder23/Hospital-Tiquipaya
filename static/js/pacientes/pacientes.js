document.addEventListener('DOMContentLoaded', function() {
    const inputBusqueda = document.getElementById('buscar-paciente');
    const selectSeguro = document.getElementById('filtro-seguro');
    const selectEstado = document.getElementById('filtro-estado');
    const selectOrdenFecha = document.getElementById('filtro-orden-fecha');
    const tabla = document.querySelector('.table.pacientes tbody');
    
    if (!tabla) return;
    
    const filas = Array.from(tabla.getElementsByTagName('tr'));

    // Función para normalizar texto (quitar acentos y convertir a minúsculas)
    function normalize(text) {
        return text.normalize('NFD')
                   .replace(/[\u0300-\u036f]/g, '')
                   .toLowerCase()
                   .trim();
    }

    // Función principal de filtrado
    function filtrarTabla() {
        const textoBusqueda = normalize(inputBusqueda ? inputBusqueda.value : '');
        const seguroSeleccionado = selectSeguro ? selectSeguro.value : '';
        const estadoSeleccionado = selectEstado ? selectEstado.value : '';
        const ordenFecha = selectOrdenFecha ? selectOrdenFecha.value : '';

        // Filtrar filas
        let filasVisibles = filas.filter(fila => {
            // Saltar fila de "empty"
            if (fila.querySelector('td[colspan]')) return false;

            const nombres = normalize(fila.getAttribute('data-nombres') || '');
            const apellidoPaterno = normalize(fila.getAttribute('data-apellido_paterno') || '');
            const apellidoMaterno = normalize(fila.getAttribute('data-apellido_materno') || '');
            const ci = normalize(fila.getAttribute('data-ci') || '');
            const seguro = fila.getAttribute('data-tiene_seguro') || '';
            const estado = fila.getAttribute('data-activo') || '';
            
            // Buscar en nombre, apellidos y CI
            const coincideBusqueda = nombres.includes(textoBusqueda) || 
                                     apellidoPaterno.includes(textoBusqueda) ||
                                     apellidoMaterno.includes(textoBusqueda) ||
                                     ci.includes(textoBusqueda);
            
            // Filtrar por seguro
            const coincideSeguro = !seguroSeleccionado || seguro === seguroSeleccionado;
            
            // Filtrar por estado
            const coincideEstado = !estadoSeleccionado || estado === estadoSeleccionado;
            
            return coincideBusqueda && coincideSeguro && coincideEstado;
        });

        // Ordenar por fecha si es necesario
        if (ordenFecha) {
            filasVisibles.sort((a, b) => {
                const fechaA = new Date(a.getAttribute('data-registrado_en'));
                const fechaB = new Date(b.getAttribute('data-registrado_en'));
                
                return ordenFecha === 'desc' ? fechaB - fechaA : fechaA - fechaB;
            });
        }

        // Ocultar todas las filas primero
        filas.forEach(fila => fila.style.display = 'none');

        // Mostrar solo las filas filtradas en el orden correcto
        filasVisibles.forEach((fila, index) => {
            fila.style.display = '';
            // Reordenar en el DOM si es necesario
            if (ordenFecha) {
                tabla.appendChild(fila);
            }
        });
    }

    // Event listeners
    if (inputBusqueda) {
        inputBusqueda.addEventListener('input', filtrarTabla);
    }

    if (selectSeguro) {
        selectSeguro.addEventListener('change', filtrarTabla);
    }

    if (selectEstado) {
        selectEstado.addEventListener('change', filtrarTabla);
    }

    if (selectOrdenFecha) {
        selectOrdenFecha.addEventListener('change', filtrarTabla);
    }
});
