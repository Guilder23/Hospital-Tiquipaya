document.addEventListener('DOMContentLoaded',function(){
  var mDelete=document.getElementById('modal-eliminar-ecografia');
  var form=document.getElementById('form-delete');
  var codigoSpan=document.getElementById('delete-codigo');
  var currentId=null;
  
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mDelete)close(mDelete)})});
  
  document.querySelectorAll('.btn-delete').forEach(function(btn){
    btn.addEventListener('click',function(){
      var row=this.closest('tr');
      currentId=row.getAttribute('data-id');
      var codigo=row.getAttribute('data-codigo');
      codigoSpan.textContent=codigo;
      form.action='/ecografias/'+currentId+'/eliminar/';
      open(mDelete);
    });
  });
});
