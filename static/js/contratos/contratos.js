document.addEventListener('DOMContentLoaded', function() {
    const inputBusqueda = document.getElementById('buscar-contrato');
    const selectEstado = document.getElementById('filtro-estado');
    const tabla = document.querySelector('.table.contratos tbody');
    
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
        const estadoSeleccionado = selectEstado ? selectEstado.value : '';

        // Filtrar filas
        let filasVisibles = filas.filter(fila => {
            // Saltar fila de "empty"
            if (fila.querySelector('td[colspan]')) return false;

            const nombre = normalize(fila.getAttribute('data-nombre') || '');
            const estado = fila.getAttribute('data-estado') || '';
            
            // Buscar en nombre
            const coincideBusqueda = nombre.includes(textoBusqueda);
            
            // Filtrar por estado (comparar string "True" o "False" con "true" o "false")
            const coincideEstado = !estadoSeleccionado || estado.toLowerCase() === estadoSeleccionado;
            
            return coincideBusqueda && coincideEstado;
        });

        // Ocultar todas las filas primero
        filas.forEach(fila => fila.style.display = 'none');

        // Mostrar solo las filas filtradas
        filasVisibles.forEach(fila => {
            fila.style.display = '';
        });
    }

    // Event listeners
    if (inputBusqueda) {
        inputBusqueda.addEventListener('input', filtrarTabla);
    }

    if (selectEstado) {
        selectEstado.addEventListener('change', filtrarTabla);
    }
});
