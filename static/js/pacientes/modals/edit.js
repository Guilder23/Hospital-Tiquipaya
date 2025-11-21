document.addEventListener('DOMContentLoaded',function(){
  var mEdit=document.getElementById('modal-editar-paciente');
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mEdit)close(mEdit)})})
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
      setVal('emergencia_nombre', row.getAttribute('data-emergencia_nombre'));
      setVal('emergencia_telefono', row.getAttribute('data-emergencia_telefono'));
      setVal('emergencia_relacion', row.getAttribute('data-emergencia_relacion'));
      setVal('activo', row.getAttribute('data-activo')==='True'?'True':'False');
      open(mEdit);
    })
  })
});