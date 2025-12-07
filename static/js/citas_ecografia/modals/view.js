// JavaScript para modal de ver detalles

document.addEventListener('DOMContentLoaded', function() {
    const viewButtons = document.querySelectorAll('.btn-view');
    const modalView = new bootstrap.Modal(document.getElementById('modal-view'));

    viewButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const row = this.closest('tr');
            mostrarDetalles(row, modalView);
        });
    });
});

function mostrarDetalles(row, modalView) {
    const paciente = row.getAttribute('data-paciente');
    const ci = row.getAttribute('data-ci');
    const especialidad = row.getAttribute('data-especialidad');
    const medico = row.getAttribute('data-medico');
    const fecha = row.getAttribute('data-fecha');
    const hora = row.getAttribute('data-hora');
    const estado = row.getAttribute('data-estado');
    const comentario = row.getAttribute('data-comentario') || 'No hay comentarios';
    const resultado = row.getAttribute('data-resultado') || 'Pendiente';

    // Convertir fecha a formato legible
    const fechaObj = new Date(fecha);
    const fechaFormato = fechaObj.toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });

    // Convertir estado
    const estadoTexto = getEstadoTexto(estado);

    document.getElementById('view-paciente').textContent = paciente;
    document.getElementById('view-ci').textContent = ci;
    document.getElementById('view-especialidad').textContent = especialidad;
    document.getElementById('view-medico').textContent = medico;
    document.getElementById('view-fecha').textContent = fechaFormato;
    document.getElementById('view-hora').textContent = hora;
    document.getElementById('view-estado').textContent = estadoTexto;
    document.getElementById('view-comentario').textContent = comentario;
    document.getElementById('view-resultado').textContent = resultado;

    modalView.show();
}

function getEstadoTexto(estado) {
    const estadoMap = {
        'PROGRAMADA': 'Programada',
        'REALIZADA': 'Realizada',
        'CANCELADA': 'Cancelada',
        'REPROGRAMADA': 'Reprogramada'
    };
    return estadoMap[estado] || estado;
}
