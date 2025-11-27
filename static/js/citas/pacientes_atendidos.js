// JavaScript para Pacientes Atendidos

// Función para filtrar tabla por especialidad
function filtrarPorEspecialidad() {
    const filtro = document.getElementById('filtroEspecialidad');
    if (!filtro) return;

    filtro.addEventListener('change', function() {
        const valor = this.value.toLowerCase();
        const filas = document.querySelectorAll('.table tbody tr');

        filas.forEach(fila => {
            if (valor === '' || fila.textContent.toLowerCase().includes(valor)) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }
        });
    });
}

// Función para filtrar tabla por nombre de paciente
function filtrarPorPaciente() {
    const filtro = document.getElementById('filtroPaciente');
    if (!filtro) return;

    filtro.addEventListener('keyup', function() {
        const valor = this.value.toLowerCase();
        const filas = document.querySelectorAll('.table tbody tr');

        filas.forEach(fila => {
            const paciente = fila.querySelector('td:first-child').textContent.toLowerCase();
            if (paciente.includes(valor)) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }
        });
    });
}

// Función para exportar tabla a CSV
function exportarACSV() {
    const tabla = document.querySelector('.table');
    if (!tabla) return;

    let csv = [];
    let filas = tabla.querySelectorAll('tr');

    filas.forEach(fila => {
        let fila_csv = [];
        let celdas = fila.querySelectorAll('td, th');

        celdas.forEach(celda => {
            fila_csv.push('"' + celda.textContent.trim() + '"');
        });

        csv.push(fila_csv.join(','));
    });

    const csv_string = csv.join('\n');
    const blob = new Blob([csv_string], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pacientes_atendidos.csv';
    a.click();
}

// Función para imprimir tabla
function imprimirTabla() {
    const printWindow = window.open('', '', 'width=900,height=600');
    const tabla = document.querySelector('.table').outerHTML;
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pacientes Atendidos</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { font-size: 12px; }
                table { width: 100%; }
            </style>
        </head>
        <body onload="window.print()">
            ${tabla}
        </body>
        </html>
    `);
    printWindow.document.close();
}

// Función para ordenar tabla por columna
function ordenarTabla(columna) {
    const tabla = document.querySelector('.table tbody');
    if (!tabla) return;

    const filas = Array.from(tabla.querySelectorAll('tr'));
    const ordenadas = filas.sort((a, b) => {
        const celdaA = a.children[columna]?.textContent.trim() || '';
        const celdaB = b.children[columna]?.textContent.trim() || '';
        return celdaA.localeCompare(celdaB);
    });

    ordenadas.forEach(fila => tabla.appendChild(fila));
}

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    filtrarPorEspecialidad();
    filtrarPorPaciente();

    // Agregar eventos a headers para ordenar
    const headers = document.querySelectorAll('.table th');
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', () => ordenarTabla(index));
    });
});

// Exportar funciones globales
window.exportarACSV = exportarACSV;
window.imprimirTabla = imprimirTabla;
