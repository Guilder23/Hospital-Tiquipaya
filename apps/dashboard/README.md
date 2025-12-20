# 📊 Dashboard Administrativo - Hospital Tiquipaya

## 🎯 Descripción

Dashboard completo para administradores del Hospital Tiquipaya que proporciona una visión integral de todas las operaciones del hospital.

## 📂 Estructura del Proyecto

```
apps/dashboard/
├── __init__.py
├── apps.py
├── admin.py
├── models.py
├── views.py
├── urls.py
└── tests.py

templates/dashboard/
├── dashboard.html
└── no_acceso.html

static/
├── css/dashboard/
│   └── dashboard.css
└── js/dashboard/
    └── dashboard.js
```

## 🚀 Características

El dashboard incluye las siguientes métricas y gráficos:

### 📊 Estadísticas Principales

1. **Pacientes**
   - Total de pacientes registrados
   - Pacientes activos (con citas programadas)
   - Pacientes con seguro
   - Pacientes sin seguro
   - Distribución por género

2. **Citas**
   - Total de citas
   - Citas programadas hoy
   - Citas completadas
   - Citas canceladas
   - Comparativa mes actual vs mes pasado
   - Citas por tipo (Consulta/Ecografía)
   - Citas por estado
   - Duración promedio de atención

3. **Médicos**
   - Total de médicos
   - Médicos activos
   - Top 5 médicos con más citas

4. **Ecografías**
   - Total de ecografías
   - Ecografías completadas
   - Ecografías pendientes

5. **Especialidades**
   - Total de especialidades
   - Top 5 especialidades más solicitadas

6. **Sistema**
   - Total de usuarios
   - Administradores
   - Contratos totales
   - Contratos vigentes

### 📈 Gráficos Disponibles

1. **Línea**: Citas en los últimos 7 días
2. **Donut**: Citas por tipo, Cobertura de seguros
3. **Barra Horizontal**: Top 5 especialidades, Top 5 médicos
4. **Barra Vertical**: Citas por estado, Comparativa mensual
5. **Pie**: Pacientes por género

## 🔧 Instalación

### 1. Agregar a INSTALLED_APPS

El dashboard ya está agregado a `hospital_tiquipaya/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'apps.dashboard',
]
```

### 2. Configurar URLs

Las URLs ya están configuradas en `hospital_tiquipaya/urls.py`:

```python
path('dashboard/', include('apps.dashboard.urls')),
```

### 3. Ejecutar migraciones (si es necesario)

```bash
python manage.py migrate
```

### 4. Acceder al Dashboard

- URL: `http://localhost:8000/dashboard/`
- API de datos: `http://localhost:8000/dashboard/api/data/`

## 🔐 Seguridad

El dashboard solo es accesible para usuarios autenticados que sean **administradores** (is_staff=True).

- Si el usuario no está autenticado, será redirigido a la página de login
- Si el usuario no es administrador, verá una página de acceso denegado

## 🎨 Diseño

- **Framework CSS**: CSS3 personalizado
- **Gráficos**: Chart.js 3.9.1
- **Colores**: Paleta moderna y coherente
- **Responsive**: Adaptable a dispositivos móviles
- **Animaciones**: Transiciones suaves y efectos visuales

## 📱 Colores Utilizados

```
Primario:    #2563eb (Azul)
Secundario:  #64748b (Gris)
Éxito:       #10b981 (Verde)
Advertencia: #f59e0b (Naranja)
Peligro:     #ef4444 (Rojo)
Info:        #0ea5e9 (Cyan)
Púrpura:     #8b5cf6 (Púrpura)
Rosa:        #ec4899 (Rosa)
```

## 🔄 Actualización de Datos

Los datos se cargan automáticamente al abrir el dashboard y se actualizan cada **5 minutos**.

Para recargar manualmente, recarga la página o abre el inspector del navegador y ejecuta:

```javascript
loadDashboardData();
```

## 📊 API Endpoint

### GET /dashboard/api/data/

Devuelve un JSON con todas las estadísticas:

```json
{
  "pacientes": {
    "total": 100,
    "activos": 45,
    "con_seguro": 60,
    "sin_seguro": 40,
    "por_genero": {"M": 55, "F": 45}
  },
  "citas": {
    "total": 500,
    "hoy": 12,
    "programadas": 250,
    "canceladas": 25,
    "completadas": 225,
    ...
  },
  ...
}
```

## 🛠️ Personalización

### Cambiar colores

Edita los colores en `/static/css/dashboard/dashboard.css`:

```css
:root {
    --color-primary: #2563eb;
    --color-secondary: #64748b;
    ...
}
```

### Agregar nuevas estadísticas

1. En `views.py`, agrega el cálculo de la estadística
2. En el JSON de respuesta, incluye la nueva métrica
3. En `dashboard.html`, agrega un nuevo card
4. En `dashboard.js`, actualiza la función `populateDashboard()`

### Agregar nuevos gráficos

1. En `dashboard.html`, agrega un nuevo elemento `<canvas>`
2. En `dashboard.js`, crea una nueva función en `createCharts()`

## 🐛 Debugging

Para ver los datos JSON en la consola:

```javascript
loadDashboardData();
```

Abre las DevTools (F12) y verás los datos en la pestaña "Network" → "dashboard"

## 📝 Notas

- Las estadísticas se calculan en tiempo real desde la base de datos
- El dashboard es **read-only** (no permite modificar datos)
- Los datos se cachean en el navegador pero se recargan automáticamente
- Compatible con SQLite, PostgreSQL y MySQL

## 🚀 Próximas Mejoras

- [ ] Exportar reportes a PDF
- [ ] Filtros por rango de fechas
- [ ] Gráficos interactivos con zoom
- [ ] Alertas en tiempo real
- [ ] Comparativas año a año
- [ ] Análisis predictivos

---

**Versión**: 1.0  
**Última actualización**: 20 de diciembre de 2025
