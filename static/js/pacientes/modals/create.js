document.addEventListener('DOMContentLoaded',function(){
  var mCreate=document.getElementById('modal-crear-paciente');
  var btnOpenCreate=document.getElementById('btn-open-create');
  var form=document.getElementById('form-create');
  var errorBox=document.getElementById('create-error');
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mCreate)close(mCreate)})})
  if(btnOpenCreate){btnOpenCreate.addEventListener('click',function(){open(mCreate)})}
  
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
  
  if(form){
    // Seguro: habilitar/deshabilitar y mostrar tipo
    var selTiene = document.getElementById('crear-tiene-seguro');
    var inpNumero = document.getElementById('crear-numero-seguro');
    var tipoRow = document.getElementById('crear-tipo-seguro-row');
    function syncSeguroUI(){
      var v = selTiene ? selTiene.value : 'False';
      var activo = (v === 'True');
      if(inpNumero){ inpNumero.disabled = !activo; if(!activo){ inpNumero.value=''; } }
      if(tipoRow){ tipoRow.style.display = activo ? 'block' : 'none'; }
    }
    if(selTiene){ selTiene.addEventListener('change', syncSeguroUI); syncSeguroUI(); }

    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(errorBox){ errorBox.style.display='none'; errorBox.textContent=''; }
      var fd=new FormData(form);
      // Enviar valores tal cual sin transformar 'tiene_seguro'
      fetch(form.getAttribute('action'),{ method:'POST', body:fd, credentials:'same-origin' })
        .then(function(res){
          if(res.status<400){
            try{ localStorage.setItem('toast_message','Paciente creado'); localStorage.setItem('toast_type','success'); }catch(e){}
            close(mCreate);
            setTimeout(function(){ window.location.reload(); }, 600);
            return null;
          }
          return res.json();
        })
        .then(function(data){ 
          if(data===null) return; 
          if(errorBox){ 
            var msgs = [];
            for(var field in data){
              if(data.hasOwnProperty(field)){
                msgs.push(field + ': ' + data[field].join(', '));
              }
            }
            errorBox.textContent = msgs.length > 0 ? msgs.join(' | ') : 'Error al guardar. Verifica los datos.'; 
            errorBox.style.display='block'; 
          } 
        })
        .catch(function(){ if(errorBox){ errorBox.textContent='Error de conexión'; errorBox.style.display='block'; } });
    });
  }
});
