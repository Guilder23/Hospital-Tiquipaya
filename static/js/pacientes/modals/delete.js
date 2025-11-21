document.addEventListener('DOMContentLoaded',function(){
  var mDelete=document.getElementById('modal-eliminar-paciente');
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mDelete)close(mDelete)})})
  document.querySelectorAll('.btn-delete').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var ci=btn.getAttribute('data-ci');
      var f=document.getElementById('form-delete');
      f.setAttribute('action','/pacientes/'+id+'/eliminar/');
      var t=document.getElementById('delete-text'); if(t){t.textContent='¿Confirmas desactivar CI '+ci+'?'}
      open(mDelete);
    })
  })
});