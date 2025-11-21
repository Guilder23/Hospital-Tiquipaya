document.addEventListener('DOMContentLoaded',function(){
  var mEdit=document.getElementById('modal-editar-paciente');
  function open(m){m.setAttribute('aria-hidden','false')}
  function close(m){m.setAttribute('aria-hidden','true')}
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mEdit)close(mEdit)})})
  document.querySelectorAll('.btn-edit').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var row=document.querySelector('tr[data-id="'+id+'"]');
      var f=document.getElementById('form-edit');
      f.setAttribute('action','/pacientes/'+id+'/editar/');
      f.querySelector('[name="ci"]').value=row.getAttribute('data-ci')||'';
      f.querySelector('[name="expedido"]').value=row.getAttribute('data-expedido')||'';
      f.querySelector('[name="nombres"]').value=row.getAttribute('data-nombres')||'';
      f.querySelector('[name="apellidos"]').value=row.getAttribute('data-apellidos')||'';
      f.querySelector('[name="fecha_nacimiento"]').value=row.getAttribute('data-fecha_nacimiento')||'';
      f.querySelector('[name="genero"]').value=row.getAttribute('data-genero')||'';
      f.querySelector('[name="nacionalidad"]').value=row.getAttribute('data-nacionalidad')||'';
      f.querySelector('[name="telefono"]').value=row.getAttribute('data-telefono')||'';
      f.querySelector('[name="email"]').value=row.getAttribute('data-email')||'';
      f.querySelector('[name="direccion"]').value=row.getAttribute('data-direccion')||'';
      var ts=row.getAttribute('data-tiene_seguro')==='True'?'True':'False';
      f.querySelector('[name="tiene_seguro"]').value=ts;
      f.querySelector('[name="numero_seguro"]').value=row.getAttribute('data-numero_seguro')||'';
      f.querySelector('[name="emergencia_nombre"]').value=row.getAttribute('data-emergencia_nombre')||'';
      f.querySelector('[name="emergencia_telefono"]').value=row.getAttribute('data-emergencia_telefono')||'';
      f.querySelector('[name="emergencia_relacion"]').value=row.getAttribute('data-emergencia_relacion')||'';
      open(mEdit);
    })
  })
});