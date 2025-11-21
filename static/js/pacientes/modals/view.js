document.addEventListener('DOMContentLoaded',function(){
  var mView=document.getElementById('modal-ver-paciente');
  function open(m){m.setAttribute('aria-hidden','false')}
  function close(m){m.setAttribute('aria-hidden','true')}
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mView)close(mView)})})
  document.querySelectorAll('.btn-view').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var row=document.querySelector('tr[data-id="'+id+'"]');
      function set(idSel, val){var el=document.getElementById(idSel); if(el) el.textContent=val||''}
      set('view-ci', row.getAttribute('data-ci'));
      set('view-expedido', row.getAttribute('data-expedido'));
      set('view-nombres', row.getAttribute('data-nombres'));
      set('view-apellidos', row.getAttribute('data-apellidos'));
      set('view-fecha_nacimiento', row.getAttribute('data-fecha_nacimiento'));
      var gen=row.getAttribute('data-genero'); set('view-genero', gen==='M'?'Masculino':(gen==='F'?'Femenino':''));
      set('view-nacionalidad', row.getAttribute('data-nacionalidad'));
      set('view-telefono', row.getAttribute('data-telefono'));
      set('view-email', row.getAttribute('data-email'));
      set('view-direccion', row.getAttribute('data-direccion'));
      set('view-tiene_seguro', row.getAttribute('data-tiene_seguro')==='True'?'Sí':'No');
      set('view-numero_seguro', row.getAttribute('data-numero_seguro'));
      set('view-emergencia_nombre', row.getAttribute('data-emergencia_nombre'));
      set('view-emergencia_telefono', row.getAttribute('data-emergencia_telefono'));
      set('view-emergencia_relacion', row.getAttribute('data-emergencia_relacion'));
      open(mView);
    })
  })
});