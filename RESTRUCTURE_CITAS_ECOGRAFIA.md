# Restructuración de Templates - Citas Ecografía

## Resumen de Cambios

Se ha reestructurado completamente la aplicación `citas_ecografia` para seguir el mismo patrón que la aplicación `contratos`, garantizando consistencia en toda la codebase.

## Estructura de Archivos Nueva

### Templates (`templates/citas_ecografia/`)
```
citas_ecografia/
├── list.html                    # Página principal con tabla de citas
└── modals/
    ├── create.html             # Modal multi-paso para agendar nueva cita
    ├── edit.html               # Modal para editar cita existente
    ├── view.html               # Modal para ver detalles de cita
    └── delete.html             # Modal para confirmar cancelación
```

### JavaScript (`static/js/citas_ecografia/`)
```
citas_ecografia/
└── modals/
    ├── create.js              # Lógica para agendar (búsqueda, selección, confirmación)
    ├── edit.js                # Lógica para editar cita
    ├── view.js                # Lógica para mostrar detalles
    └── delete.js              # Lógica para cancelar cita
```

### CSS (`static/css/citas_ecografia/`)
```
citas_ecografia/
├── citas_ecografia.css        # Estilos principales (tabla, botones)
└── modals/
    ├── create.css             # Estilos para modal crear
    ├── edit.css               # Estilos para modal editar
    ├── view.css               # Estilos para modal ver
    └── delete.css             # Estilos para modal eliminar
```

## Patrones Implementados

### 1. HTML Modal Pattern
Cada modal sigue la estructura de Bootstrap 5:
- Modal header con título y botón cerrar
- Modal body con contenido dinámico
- Modal footer con botones de acción
- Data attributes en filas de tabla para poblamiento rápido

### 2. JavaScript por Modal
- Funciones independientes para cada operación
- Uso de data attributes para capturar información de tabla
- CSRF token handling para seguridad
- Manejo de errores con alerts Bootstrap
- Recarga automática tras éxito

### 3. CSS Organizado
- Estilos globales en archivo principal
- Estilos específicos por modal en carpeta modals/
- Variables de color consistentes con tema Hospital
- Responsive design con grid layouts

## Flujo de Agendar Cita (Multi-paso)

### Paso 1: Búsqueda de Paciente
- Entrada: CI o nombre del paciente
- Validación: Paciente debe tener habilitada ecografía
- Salida: Información del paciente

### Paso 2: Información del Paciente
- Muestra: Nombre, CI, especialidad solicitada, comentario médico
- Opción: Volver a búsqueda

### Paso 3: Selección de Fecha y Médico
- Selecciona fecha para la cita
- Sistema carga médicos disponibles que trabajan ese día
- Selecciona médico específico

### Paso 4: Selección de Hora
- Sistema obtiene horarios disponibles del médico
- Grid visual con slots de 30 minutos
- Selección de hora activa botón confirmar

### Paso 5: Confirmación
- Botón "Agendar Cita" realiza POST a `/citas-ecografia/crear/`
- Genera código único para cita
- Recarga página tras éxito

## Endpoints API

### GET / POST Endpoints
- `POST /citas-ecografia/buscar-paciente/` - Buscar paciente
- `POST /citas-ecografia/obtener-horarios/` - Obtener horarios disponibles
- `POST /citas-ecografia/crear/` - Crear nueva cita
- `POST /citas-ecografia/<id>/editar/` - Editar cita existente
- `POST /citas-ecografia/<id>/cancelar/` - Cancelar cita

## Características de Seguridad

- ✅ Validación de permisos (solo superuser o grupo admision)
- ✅ CSRF token en todas las peticiones POST
- ✅ Validación de datos en backend
- ✅ Manejo de excepciones con mensajes seguros
- ✅ Códigos de estado HTTP apropiados

## Características de UX

- ✅ Tabla responsive con datos dinámicos
- ✅ Modales Bootstrap 5 con transiciones suaves
- ✅ Validación en tiempo real
- ✅ Feedback visual con badges de estado
- ✅ Botones de acción contextuales (ver, editar, cancelar)
- ✅ Flujo intuitivo paso a paso para agendar

## Integración con Sistema Existente

### Relaciones de Datos
- CitaEcografia → Paciente (ForeignKey)
- CitaEcografia → Medico (ForeignKey)
- CitaEcografia → Especialidad (ForeignKey)
- CitaEcografia → Cita (ForeignKey a cita consulta)

### Validaciones
- El paciente debe tener una cita consulta con `requiere_ecografia=True`
- El médico debe trabajar en el día seleccionado
- No puede haber dos citas del mismo médico en la misma hora

### Estados de Cita
- `PROGRAMADA` - Cita agendada
- `REALIZADA` - Cita completada
- `CANCELADA` - Cita cancelada
- `REPROGRAMADA` - Cita reprogramada

## Próximos Pasos Sugeridos

1. ✅ Agregar link en sidebar para staff admisión
2. ✅ Testear flujo completo de agendar cita
3. ✅ Testear edición y cancelación de citas
4. ✅ Validar permisos por grupo de usuario
5. ✅ Revisar estilos en diferentes resoluciones

## Archivos Eliminados

- `templates/citas_ecografia/agendar.html` (reemplazado por modal)
- `static/js/citas_ecografia/agendar.js` (lógica trasladada a create.js)
- `static/js/citas_ecografia/list.js` (simplificado)
- `static/css/citas_ecografia/agendar.css` (reorganizado)
- `static/css/citas_ecografia/list.css` (reorganizado)

## Notas de Implementación

- Todos los modales usan IDs consistentes (`modal-create`, `modal-edit`, etc.)
- Data attributes en tabla: `data-id`, `data-paciente`, `data-fecha`, `data-hora`, etc.
- Funciones helper compartidas: `getCookie()`, `showAlert()`
- Integración con Horarios model para slots de 30 minutos
- Manejo de zonas horarias adecuado con datetime
