// ============================================
// DASHBOARD - JAVASCRIPT
// ============================================

let charts = {};

// Colores para los gráficos
const colors = {
    primary: '#2563eb',
    secondary: '#64748b',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#0ea5e9',
    purple: '#8b5cf6',
    pink: '#ec4899',
};

// Cargar datos del dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard cargado. Obteniendo datos...');
    loadDashboardData();
});

function loadDashboardData() {
    console.log('Iniciando carga de datos desde API...');
    
    // Obtener el token CSRF
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                      getCookie('csrftoken');
    
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (csrftoken) {
        headers['X-CSRFToken'] = csrftoken;
    }
    
    fetch('/dashboard/api/data/', {
        method: 'GET',
        headers: headers,
        credentials: 'same-origin'
    })
        .then(response => {
            console.log('Respuesta recibida:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data);
            if (data.error) {
                console.error('Error en API:', data.error);
                showError('Error: ' + data.error);
            } else {
                populateDashboard(data);
            }
        })
        .catch(error => {
            console.error('Error cargando datos:', error);
            showError('Error al cargar los datos del dashboard: ' + error.message);
        });
}

// Función para obtener cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function populateDashboard(data) {
    console.log('Populando dashboard con datos:', data);
    
    // Helper function para mostrar valor o 0
    const getValue = (value, defaultValue = 0) => value !== undefined && value !== null ? value : defaultValue;
    
    try {
        // PACIENTES
        document.getElementById('total-pacientes').textContent = getValue(data.pacientes?.total);
        document.getElementById('pac-total').textContent = getValue(data.pacientes?.total);
        document.getElementById('pac-activos').textContent = getValue(data.pacientes?.activos);
        document.getElementById('pac-con-seguro').textContent = getValue(data.pacientes?.con_seguro);
        document.getElementById('pac-sin-seguro').textContent = getValue(data.pacientes?.sin_seguro);
        
        // CITAS
        document.getElementById('total-citas').textContent = getValue(data.citas?.total);
        document.getElementById('citas-hoy').textContent = getValue(data.citas?.hoy);

        const elCitasHoyAtendidas = document.getElementById('citas-hoy-atendidas');
        if (elCitasHoyAtendidas) elCitasHoyAtendidas.textContent = getValue(data.citas?.hoy_atendidas);

        const elCitasHoyEnAtencion = document.getElementById('citas-hoy-en-atencion');
        if (elCitasHoyEnAtencion) elCitasHoyEnAtencion.textContent = getValue(data.citas?.hoy_en_atencion);

        const elCitasHoyEnEspera = document.getElementById('citas-hoy-en-espera');
        if (elCitasHoyEnEspera) elCitasHoyEnEspera.textContent = getValue(data.citas?.hoy_en_espera);
        
        // MÉDICOS
        document.getElementById('total-medicos').textContent = getValue(data.medicos?.total);
        document.getElementById('med-activos').textContent = getValue(data.medicos?.activos);
        
        // ECOGRAFÍAS
        document.getElementById('total-ecografias').textContent = getValue(data.ecografias?.total);
        document.getElementById('eco-total').textContent = getValue(data.ecografias?.total);
        document.getElementById('eco-completadas').textContent = getValue(data.ecografias?.completadas);
        document.getElementById('eco-pendientes').textContent = getValue(data.ecografias?.pendientes);

        const elEcoHoy = document.getElementById('eco-hoy');
        if (elEcoHoy) elEcoHoy.textContent = getValue(data.ecografias?.hoy);

        const elEcoHoyAtendidas = document.getElementById('eco-hoy-atendidas');
        if (elEcoHoyAtendidas) elEcoHoyAtendidas.textContent = getValue(data.ecografias?.hoy_atendidas);

        const elEcoHoyEnAtencion = document.getElementById('eco-hoy-en-atencion');
        if (elEcoHoyEnAtencion) elEcoHoyEnAtencion.textContent = getValue(data.ecografias?.hoy_en_atencion);

        const elEcoHoyEnEspera = document.getElementById('eco-hoy-en-espera');
        if (elEcoHoyEnEspera) elEcoHoyEnEspera.textContent = getValue(data.ecografias?.hoy_en_espera);

        // PERSONAL
        const elEcografos = document.getElementById('total-ecografos');
        if (elEcografos) elEcografos.textContent = getValue(data.personal?.ecografos);

        const elAdmision = document.getElementById('total-admision');
        if (elAdmision) elAdmision.textContent = getValue(data.personal?.admision);

        const elEncAdm = document.getElementById('total-encargado-admision');
        if (elEncAdm) elEncAdm.textContent = getValue(data.personal?.encargado_admision);
        
        // CONTRATOS
        document.getElementById('con-total').textContent = getValue(data.contratos?.total);
        document.getElementById('con-vigentes').textContent = getValue(data.contratos?.vigentes);
        
        // ESPECIALIDADES
        document.getElementById('esp-total').textContent = getValue(data.especialidades?.total);
        
        // USUARIOS
        document.getElementById('usr-total').textContent = getValue(data.usuarios?.total);
        document.getElementById('usr-admins').textContent = getValue(data.usuarios?.admins);

        const elUsrActivos = document.getElementById('usr-activos');
        if (elUsrActivos) elUsrActivos.textContent = getValue(data.usuarios?.activos);

        const elUsrInactivos = document.getElementById('usr-inactivos');
        if (elUsrInactivos) elUsrInactivos.textContent = getValue(data.usuarios?.inactivos);

        const elTotalUsuarios = document.getElementById('total-usuarios');
        if (elTotalUsuarios) elTotalUsuarios.textContent = getValue(data.usuarios?.total);
        
        console.log('Datos poblados exitosamente. Creando gráficos...');
        
        // Crear gráficos
        createCharts(data);
    } catch (error) {
        console.error('Error al popular dashboard:', error);
        showError('Error al mostrar los datos: ' + error.message);
    }
}

function createCharts(data) {
    console.log('Iniciando creación de gráficos...');

    const commonLineOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
            legend: {
                display: true,
                labels: {
                    padding: 15,
                    font: { size: 12 }
                }
            },
            tooltip: {
                enabled: true,
                padding: 10,
                displayColors: true,
            },
            filler: {
                propagate: true
            }
        },
        scales: {
            x: {
                grid: { display: false },
                ticks: { maxTicksLimit: 10 }
            },
            y: {
                beginAtZero: true,
                grid: { color: 'rgba(100, 116, 139, 0.15)' },
                ticks: { stepSize: 1 }
            }
        }
    };
    
    // 1. GRÁFICO DE CITAS POR DÍA (LÍNEA)
    const ctxCitas = document.getElementById('citasChart');
    if (ctxCitas && data.citas?.por_dia && data.citas.por_dia.length > 0) {
        try {
            charts.citasChart = new Chart(ctxCitas, {
                type: 'line',
                data: {
                    labels: data.citas.por_dia.map(d => d.fecha),
                    datasets: [{
                        label: 'Citas',
                        data: data.citas.por_dia.map(d => d.count),
                        fill: true,
                        backgroundColor: 'rgba(37, 99, 235, 0.12)',
                        borderColor: colors.primary,
                        borderWidth: 3,
                        tension: 0.4,
                        pointBackgroundColor: colors.primary,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 3,
                        pointHoverRadius: 5,
                    }]
                },
                options: commonLineOptions
            });
            console.log('Gráfico de citas por día creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de citas:', e);
        }
    }

    // 1.b GRÁFICO DE CITAS ECOGRAFÍA POR DÍA (LÍNEA)
    const ctxEcoMes = document.getElementById('ecoMesChart');
    if (ctxEcoMes && data.ecografias?.por_dia && data.ecografias.por_dia.length > 0) {
        try {
            charts.ecoMesChart = new Chart(ctxEcoMes, {
                type: 'line',
                data: {
                    labels: data.ecografias.por_dia.map(d => d.fecha),
                    datasets: [{
                        label: 'Ecografías',
                        data: data.ecografias.por_dia.map(d => d.count),
                        fill: true,
                        backgroundColor: 'rgba(139, 92, 246, 0.12)',
                        borderColor: colors.purple,
                        borderWidth: 3,
                        tension: 0.4,
                        pointBackgroundColor: colors.purple,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 3,
                        pointHoverRadius: 5,
                    }]
                },
                options: commonLineOptions
            });
            console.log('Gráfico de ecografías por día creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de ecografías:', e);
        }
    }

    // 3. GRÁFICO DE CITAS POR ESTADO (BARRA)
    const ctxEstado = document.getElementById('estadoChart');
    if (ctxEstado && data.citas?.por_estado && Object.keys(data.citas.por_estado).length > 0) {
        try {
            const estadoColors = {
                'PROGRAMADA': colors.primary,
                'REPROGRAMADA': colors.warning,
                'CANCELADA': colors.danger,
                'REALIZADA': colors.success,
            };
            const estadoLabels = Object.keys(data.citas.por_estado);
            const estadoValues = Object.values(data.citas.por_estado);
            charts.estadoChart = new Chart(ctxEstado, {
                type: 'bar',
                data: {
                    labels: estadoLabels,
                    datasets: [{
                        label: 'Cantidad de Citas',
                        data: estadoValues,
                        backgroundColor: estadoLabels.map(l => estadoColors[l] || colors.secondary),
                        borderRadius: 8,
                        borderSkipped: false
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
            console.log('Gráfico de estado de citas creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de estado:', e);
        }
    }

    // 3.b GRÁFICO DE CITAS ECOGRAFÍA POR ESTADO (BARRA)
    const ctxEcoEstado = document.getElementById('ecoEstadoChart');
    if (ctxEcoEstado && data.ecografias?.por_estado && Object.keys(data.ecografias.por_estado).length > 0) {
        try {
            const ecoEstadoColors = {
                'PROGRAMADA': colors.primary,
                'REPROGRAMADA': colors.warning,
                'CANCELADA': colors.danger,
                'REALIZADA': colors.success,
            };
            const ecoEstadoLabels = Object.keys(data.ecografias.por_estado);
            const ecoEstadoValues = Object.values(data.ecografias.por_estado);
            charts.ecoEstadoChart = new Chart(ctxEcoEstado, {
                type: 'bar',
                data: {
                    labels: ecoEstadoLabels,
                    datasets: [{
                        label: 'Cantidad de Citas Ecografía',
                        data: ecoEstadoValues,
                        backgroundColor: ecoEstadoLabels.map(l => ecoEstadoColors[l] || colors.secondary),
                        borderRadius: 8,
                        borderSkipped: false
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
            console.log('Gráfico de estado de citas ecografía creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de estado ecografía:', e);
        }
    }

    // 4. GRÁFICO DE PACIENTES POR GÉNERO (PIE)
    const ctxGenero = document.getElementById('generoChart');
    if (ctxGenero && data.pacientes?.por_genero && Object.keys(data.pacientes.por_genero).length > 0) {
        try {
            const generoLabels = {
                'M': 'Masculino',
                'F': 'Femenino',
                'O': 'Otro'
            };
            
            charts.generoChart = new Chart(ctxGenero, {
                type: 'pie',
                data: {
                    labels: Object.keys(data.pacientes.por_genero).map(k => generoLabels[k] || k),
                    datasets: [{
                        data: Object.values(data.pacientes.por_genero),
                        backgroundColor: [colors.primary, colors.pink, colors.secondary],
                        borderColor: '#fff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
            console.log('Gráfico de género creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de género:', e);
        }
    }

    // 4.b GRÁFICO DE USUARIOS POR GÉNERO (PIE)
    const ctxUserGenero = document.getElementById('userGeneroChart');
    if (ctxUserGenero && data.usuarios?.por_genero && Object.keys(data.usuarios.por_genero).length > 0) {
        try {
            const generoLabels = {
                'M': 'Masculino',
                'F': 'Femenino',
                'O': 'Otro'
            };

            charts.userGeneroChart = new Chart(ctxUserGenero, {
                type: 'pie',
                data: {
                    labels: Object.keys(data.usuarios.por_genero).map(k => generoLabels[k] || k),
                    datasets: [{
                        data: Object.values(data.usuarios.por_genero),
                        backgroundColor: [colors.primary, colors.pink, colors.secondary],
                        borderColor: '#fff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
            console.log('Gráfico de usuarios por género creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de usuarios por género:', e);
        }
    }

    // 5. GRÁFICO DE TOP 5 ESPECIALIDADES (BARRA HORIZONTAL)
    const ctxEspecialidades = document.getElementById('especialidadesChart');
    if (ctxEspecialidades && data.citas?.por_especialidad && data.citas.por_especialidad.length > 0) {
        try {
            charts.especialidadesChart = new Chart(ctxEspecialidades, {
                type: 'bar',
                data: {
                    labels: data.citas.por_especialidad.map(e => e.especialidad__nombre),
                    datasets: [{
                        label: 'Citas',
                        data: data.citas.por_especialidad.map(e => e.count),
                        backgroundColor: colors.success,
                        borderRadius: 8
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
            console.log('Gráfico de especialidades creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de especialidades:', e);
        }
    }

    // 6. GRÁFICO DE TOP 5 MÉDICOS (BARRA HORIZONTAL)
    const ctxMedicos = document.getElementById('medicosChart');
    if (ctxMedicos && data.citas?.por_medico && data.citas.por_medico.length > 0) {
        try {
            charts.medicosChart = new Chart(ctxMedicos, {
                type: 'bar',
                data: {
                    labels: data.citas.por_medico.map(m => 
                        `${m.medico__user__first_name} ${m.medico__user__last_name}`.trim()
                    ),
                    datasets: [{
                        label: 'Citas',
                        data: data.citas.por_medico.map(m => m.count),
                        backgroundColor: colors.purple,
                        borderRadius: 8
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
            console.log('Gráfico de médicos creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de médicos:', e);
        }
    }

    // 7. GRÁFICO DE COMPARATIVA MENSUAL (COLUMNAS)
    const ctxComparativa = document.getElementById('comparativaChart');
    if (ctxComparativa) {
        try {
            charts.comparativaChart = new Chart(ctxComparativa, {
                type: 'bar',
                data: {
                    labels: ['Mes Pasado', 'Este Mes'],
                    datasets: [{
                        label: 'Citas',
                        data: [data.citas?.mes_pasado || 0, data.citas?.este_mes || 0],
                        backgroundColor: [colors.warning, colors.success],
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
            console.log('Gráfico de comparativa creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de comparativa:', e);
        }
    }

    // 8. GRÁFICO DE COBERTURA DE SEGUROS (DONUT)
    const ctxSeguro = document.getElementById('seguroChart');
    if (ctxSeguro) {
        try {
            charts.seguroChart = new Chart(ctxSeguro, {
                type: 'doughnut',
                data: {
                    labels: ['Con Seguro', 'Sin Seguro'],
                    datasets: [{
                        data: [data.pacientes?.con_seguro || 0, data.pacientes?.sin_seguro || 0],
                        backgroundColor: [colors.success, colors.danger],
                        borderColor: '#fff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
            console.log('Gráfico de seguros creado ✓');
        } catch (e) {
            console.error('Error al crear gráfico de seguros:', e);
        }
    }
    
    console.log('✓ Todos los gráficos procesados');
}

function showError(message) {
    console.error(message);
    // Mostrar alerta visual
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ef4444;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 9999;
        max-width: 400px;
    `;
    errorDiv.textContent = '[ERROR] ' + message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Recargar datos cada 5 minutos
setInterval(loadDashboardData, 5 * 60 * 1000);
