# 📋 INVESTIGACIÓN Y SOLUCIÓN: Sistema de Permisos

## Cronología de la Investigación

### 1. Problema Reportado
- **Síntoma**: Usuarios con permisos "editor" NO veían botones para crear/editar/eliminar
- **Esperado**: Botones "Nueva Especialidad", "Editar", "Desactivar" para usuarios "editor"
- **Actual**: Solo veían botón "Ver" (como si tuvieran "solo_vista")

### 2. Investigación Inicial
- ✅ Base de datos: Permisos correctamente guardados como "editor"
- ✅ Middleware: Lógica correcta en simulación
- ✅ Template: Condicional correcto (`{% if user.is_superuser or permiso_actual.puede_editar %}`)
- ❌ Pero: `permiso_actual` era `None` en el HTML real

### 3. Encontrar la Causa
**Descubrimiento clave**: En el output HTML:
```
data-middleware-ejecutado="False"
```

El middleware **NO estaba siendo ejecutado** para `/especialidades/`.

Pero luego se descubrió que SÍ se estaba ejecutando, pero **saltaba temprano** porque detectaba `/especialidades/` como ruta "pública".

### 4. La Causa Raíz
En `apps/permisos/middleware.py`:

```python
RUTAS_PUBLICAS = ['/admin/', '/accounts/login/', '/accounts/logout/', '/static/', '/media/', '/']
```

El `'/'` al final causaba que **TODAS las URLs empezando con `/` fueran saltadas**:

```python
'/especialidades/'.startswith('/') == True  # BUG: El middleware se salta
```

### 5. La Solución
Cambiar a:
```python
RUTAS_PUBLICAS = ['/admin/', '/accounts/login/', '/accounts/logout/', '/static/', '/media/']
```

Y manejar la home explícitamente:
```python
if request.path == '/' or any(request.path.startswith(ruta) for ruta in self.RUTAS_PUBLICAS):
```

## Archivos Creados Durante la Investigación

Estos archivos fueron creados para diagnosticar el problema (se pueden borrar después):

1. `diagnostico_asignacion_permisos.py` - Verificar permisos en BD
2. `diagnostico_permisos_bd.py` - Listar permisos por tipo de usuario
3. `simulacion_especialidades.py` - Simular el flujo completo
4. `simulacion_vista_real.py` - Simular con RequestFactory
5. `test_permisos_real.py` - Test directo del modelo
6. `test_middleware_logging.py` - Test con client HTTP
7. `test_obtener_modulo.py` - Probar obtener_modulo_por_url
8. `extraer_html_botones.py` - Analizar HTML generado
9. `verificar_html_especialidades.py` - Verificar salida HTML del servidor
10. `verificar_urls_modulos.py` - Verificar URLs en BD
11. `matriz_permisos_nueva.py` - Script no clasificado
12. `test_nueva_funcion.py` - Script no clasificado

## Estado Final

✅ **SOLUCIONADO**: Los botones ahora aparecen correctamente para usuarios con permisos "editor"

### Verificación Final
```
✓ Permiso asignado: Encargado de Admision → Gestion de Especialidades = editor
✅ Botón 'Nueva Especialidad' aparece
✅ Botones 'Editar' aparecen  
✅ Botones 'Desactivar/Activar' aparecen
```

## Cambios Realizados

**Archivo modificado**: `apps/permisos/middleware.py`

```python
# Antes:
RUTAS_PUBLICAS = [
    '/admin/',
    '/accounts/login/',
    '/accounts/logout/',
    '/static/',
    '/media/',
    '/',  # ❌ BUG
]

# Después:
RUTAS_PUBLICAS = [
    '/admin/',
    '/accounts/login/',
    '/accounts/logout/',
    '/static/',
    '/media/',
]

# Y el condicional:
if request.path == '/' or any(request.path.startswith(ruta) for ruta in self.RUTAS_PUBLICAS):
```

## Lecciones Aprendidas

1. **Cuidado con `startswith()` en listas**: Un patrón muy general (como `'/'`) puede encubrir intenciones
2. **El orden importa**: Los middlewares se aplican en orden, así que un bug en uno afecta todo lo demás
3. **El debugging requiere múltiples niveles**: Base de datos → Middleware → Template → HTML final

