document.addEventListener('DOMContentLoaded',function(){
  var mView=document.getElementById('modal-ver-paciente');
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mView)close(mView)})})
  document.querySelectorAll('.btn-view').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var row=document.querySelector('tr[data-id="'+id+'"]');
      function set(idSel, val){var el=document.getElementById(idSel); if(el) el.textContent=val||''}
      set('view-ci', row.getAttribute('data-ci'));
      set('view-ci_complemento', row.getAttribute('data-ci_complemento'));
      set('view-expedido', row.getAttribute('data-expedido'));
      set('view-nombres', row.getAttribute('data-nombres'));
      set('view-apellido_paterno', row.getAttribute('data-apellido_paterno'));
      set('view-apellido_materno', row.getAttribute('data-apellido_materno'));
      set('view-fecha_nacimiento', row.getAttribute('data-fecha_nacimiento'));
      var gen=row.getAttribute('data-genero'); set('view-genero', gen==='M'?'Masculino':(gen==='F'?'Femenino':(gen==='O'?'Otro':'')));
      set('view-nacionalidad', row.getAttribute('data-nacionalidad'));
      set('view-telefono_fijo', row.getAttribute('data-telefono_fijo'));
      set('view-celular', row.getAttribute('data-celular'));
      set('view-email', row.getAttribute('data-email'));
      set('view-zona', row.getAttribute('data-zona'));
      set('view-calle', row.getAttribute('data-calle'));
      set('view-numero_domicilio', row.getAttribute('data-numero_domicilio'));
      set('view-direccion', row.getAttribute('data-direccion'));
      set('view-tiene_seguro', row.getAttribute('data-tiene_seguro')==='True'?'Sí':'No');
      set('view-numero_seguro', row.getAttribute('data-numero_seguro'));
      set('view-emergencia_nombre', row.getAttribute('data-emergencia_nombre'));
      set('view-emergencia_telefono', row.getAttribute('data-emergencia_telefono'));
      set('view-emergencia_relacion', row.getAttribute('data-emergencia_relacion'));
      set('view-numero_boleta_sus', row.getAttribute('data-numero_boleta_sus'));
      set('view-numero_carnet_historial', row.getAttribute('data-numero_carnet_historial'));
      set('view-numero_boleta_referencia', row.getAttribute('data-numero_boleta_referencia'));
      set('view-numero_copias', row.getAttribute('data-numero_copias'));
      set('view-activo', row.getAttribute('data-activo')==='True'?'Activo':'Inactivo');
      set('view-registrado_en', row.getAttribute('data-registrado_en'));
      open(mView);
    })
  })
});