document.addEventListener('DOMContentLoaded', function() {
    const inputBusqueda = document.getElementById('buscar-tipo');
    const selectOrdenFecha = document.getElementById('filtro-orden-fecha');
    const tabla = document.querySelector('.table tbody');
    
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
        const ordenFecha = selectOrdenFecha ? selectOrdenFecha.value : '';

        // Filtrar filas
        let filasVisibles = filas.filter(fila => {
            // Saltar fila de "empty"
            if (fila.querySelector('td[colspan]')) return false;
            
            const nombre = normalize(fila.getAttribute('data-nombre') || '');
            const descripcion = normalize(fila.getAttribute('data-descripcion') || '');
            
            // Buscar en nombre y descripción
            const coincideBusqueda = nombre.includes(textoBusqueda) || 
                                     descripcion.includes(textoBusqueda);
            
            return coincideBusqueda;
        });

        // Ordenar por fecha si es necesario
        if (ordenFecha) {
            filasVisibles.sort((a, b) => {
                const fechaA = new Date(a.getAttribute('data-creado_en'));
                const fechaB = new Date(b.getAttribute('data-creado_en'));
                
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

    if (selectOrdenFecha) {
        selectOrdenFecha.addEventListener('change', filtrarTabla);
    }
});
