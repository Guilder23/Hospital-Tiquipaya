document.addEventListener('DOMContentLoaded',function(){
  var mEdit=document.getElementById('modal-editar-paciente');
  var form=document.getElementById('form-edit');
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mEdit)close(mEdit)})})
  
  // ========== VALIDACIONES EN TIEMPO REAL ==========
  if(form){
    // Establecer fecha máxima en fecha de nacimiento (hoy)
    var fechaNacInput = form.querySelector('[name="fecha_nacimiento"]');
    if(fechaNacInput){
      var hoy = new Date();
      var fechaMax = hoy.toISOString().split('T')[0];
      fechaNacInput.setAttribute('max', fechaMax);
    }

    // Validar campos alfabéticos (nombres, apellidos, nacionalidad)
    var camposAlfabeticos = form.querySelectorAll('[name="nombres"], [name="apellido_paterno"], [name="apellido_materno"], [name="nacionalidad"], [name="emergencia_nombre"], [name="emergencia_relacion"]');
    camposAlfabeticos.forEach(function(input) {
      input.addEventListener('input', function() {
        var regex = /[^A-Za-záéíóúÁÉÍÓÚñÑ\s]/g;
        if (regex.test(this.value)) {
          this.value = this.value.replace(regex, '');
        }
      });
    });

    // Validar CI (solo números, 7-8 dígitos)
    var ciInput = form.querySelector('[name="ci"]');
    if(ciInput){
      ciInput.addEventListener('input', function() {
        var regex = /[^0-9]/g;
        if (regex.test(this.value)) {
          this.value = this.value.replace(regex, '');
        }
        if (this.value.length > 8) {
          this.value = this.value.slice(0, 8);
        }
      });
    }

    // Validar complemento CI (alfanumérico, 2-4 caracteres)
    var complementoInput = form.querySelector('[name="ci_complemento"]');
    if(complementoInput){
      complementoInput.addEventListener('input', function() {
        var regex = /[^A-Za-z0-9]/g;
        if (regex.test(this.value)) {
          this.value = this.value.replace(regex, '');
        }
        if (this.value.length > 4) {
          this.value = this.value.slice(0, 4);
        }
      });
    }

    // Validar teléfonos (solo números, 8 dígitos)
    var telefonosInputs = form.querySelectorAll('[name="telefono_fijo"], [name="celular"], [name="emergencia_telefono"]');
    telefonosInputs.forEach(function(input) {
      input.addEventListener('input', function() {
        var regex = /[^0-9]/g;
        if (regex.test(this.value)) {
          this.value = this.value.replace(regex, '');
        }
        if (this.value.length > 8) {
          this.value = this.value.slice(0, 8);
        }
      });
    });

    // Validar campos alfanuméricos (zona, calle, número)
    var camposAlfanumericos = form.querySelectorAll('[name="zona"], [name="calle"], [name="numero_domicilio"]');
    camposAlfanumericos.forEach(function(input) {
      input.addEventListener('input', function() {
        var regex = /[^A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]/g;
        if (regex.test(this.value)) {
          this.value = this.value.replace(regex, '');
        }
      });
    });

    // Validar dirección (alfanuméricos + puntuación)
    var direccionInput = form.querySelector('[name="direccion"]');
    if(direccionInput){
      direccionInput.addEventListener('input', function() {
        var regex = /[^A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s.,;:¿?¡!()-]/g;
        if (regex.test(this.value)) {
          this.value = this.value.replace(regex, '');
        }
      });
    }

    // Validar números de documentos médicos (solo números)
    var numerosDocumentos = form.querySelectorAll('[name="numero_seguro"], [name="numero_boleta_sus"], [name="numero_carnet_historial"], [name="numero_boleta_referencia"], [name="numero_copias"]');
    numerosDocumentos.forEach(function(input) {
      input.addEventListener('input', function() {
        var regex = /[^0-9]/g;
        if (regex.test(this.value)) {
          this.value = this.value.replace(regex, '');
        }
      });
    });
  }
  document.querySelectorAll('.btn-edit').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var row=document.querySelector('tr[data-id="'+id+'"]');
      var f=document.getElementById('form-edit');
      f.setAttribute('action','/pacientes/'+id+'/editar/');
      function setVal(name, val){ var el=f.querySelector('[name="'+name+'"]'); if(el){ el.value=val||''; } }
      setVal('nombres', row.getAttribute('data-nombres'));
      setVal('apellido_paterno', row.getAttribute('data-apellido_paterno'));
      setVal('apellido_materno', row.getAttribute('data-apellido_materno'));
      setVal('ci', row.getAttribute('data-ci'));
      setVal('ci_complemento', row.getAttribute('data-ci_complemento'));
      setVal('expedido', row.getAttribute('data-expedido'));
      setVal('fecha_nacimiento', row.getAttribute('data-fecha_nacimiento'));
      setVal('genero', row.getAttribute('data-genero'));
      setVal('nacionalidad', row.getAttribute('data-nacionalidad'));
      setVal('telefono_fijo', row.getAttribute('data-telefono_fijo'));
      setVal('celular', row.getAttribute('data-celular'));
      setVal('email', row.getAttribute('data-email'));
      setVal('zona', row.getAttribute('data-zona'));
      setVal('calle', row.getAttribute('data-calle'));
      setVal('numero_domicilio', row.getAttribute('data-numero_domicilio'));
      setVal('direccion', row.getAttribute('data-direccion'));
      var ts=row.getAttribute('data-tiene_seguro')==='True'?'True':'False';
      setVal('tiene_seguro', ts);
      setVal('numero_seguro', row.getAttribute('data-numero_seguro'));
      setVal('tipo_seguro', row.getAttribute('data-tipo_seguro'));
      setVal('emergencia_nombre', row.getAttribute('data-emergencia_nombre'));
      setVal('emergencia_telefono', row.getAttribute('data-emergencia_telefono'));
      setVal('emergencia_relacion', row.getAttribute('data-emergencia_relacion'));
      setVal('numero_boleta_sus', row.getAttribute('data-numero_boleta_sus'));
      setVal('numero_carnet_historial', row.getAttribute('data-numero_carnet_historial'));
      setVal('numero_boleta_referencia', row.getAttribute('data-numero_boleta_referencia'));
      setVal('numero_copias', row.getAttribute('data-numero_copias'));
      setVal('activo', row.getAttribute('data-activo')==='True'?'True':'False');
      open(mEdit);

      // Seguro: habilitar/deshabilitar y mostrar tipo
      var selTiene = document.getElementById('editar-tiene-seguro');
      var inpNumero = document.getElementById('editar-numero-seguro');
      var tipoRow = document.getElementById('editar-tipo-seguro-row');
      function syncSeguroUI(){
        var v = selTiene ? selTiene.value : 'False';
        var activo = (v === 'True');
        if(inpNumero){ inpNumero.disabled = !activo; if(!activo){ inpNumero.value=''; } }
        if(tipoRow){ tipoRow.style.display = activo ? 'block' : 'none'; }
      }
      if(selTiene){ selTiene.addEventListener('change', syncSeguroUI); syncSeguroUI(); }
    })
  })
});
