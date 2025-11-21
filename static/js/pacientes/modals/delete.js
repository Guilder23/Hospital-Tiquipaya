document.addEventListener('DOMContentLoaded',function(){
  var mDelete=document.getElementById('modal-eliminar-paciente');
  function open(m){m.setAttribute('aria-hidden','false')}
  function close(m){m.setAttribute('aria-hidden','true')}
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mDelete)close(mDelete)})})
  document.querySelectorAll('.btn-delete').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var ci=btn.getAttribute('data-ci');
      var f=document.getElementById('form-delete');
      f.setAttribute('action','/pacientes/'+id+'/eliminar/');
      var t=document.getElementById('delete-text'); if(t){t.textContent='¿Confirmas eliminar CI '+ci+'?'}
      open(mDelete);
    })
  })
});