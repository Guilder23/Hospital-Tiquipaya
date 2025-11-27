document.addEventListener('DOMContentLoaded',function(){
  var mEdit=document.getElementById('modal-editar-ecografia');
  var form=document.getElementById('form-edit');
  var errorBox=document.getElementById('edit-error');
  var codigoInput=document.getElementById('edit-codigo');
  var nombreInput=document.getElementById('edit-nombre');
  var medicoInput=document.getElementById('edit-medico');
  var especialidadInput=document.getElementById('edit-especialidad');
  var descripcionInput=document.getElementById('edit-descripcion');
  var estadoInput=document.getElementById('edit-estado');
  var currentId=null;
  
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mEdit)close(mEdit)})});
  
  document.querySelectorAll('.btn-edit').forEach(function(btn){
    btn.addEventListener('click',function(){
      var row=this.closest('tr');
      currentId=row.getAttribute('data-id');
      codigoInput.value=row.getAttribute('data-codigo');
      nombreInput.value=row.getAttribute('data-nombre');
      medicoInput.value=row.getAttribute('data-medico_id');
      especialidadInput.value=row.getAttribute('data-especialidad_id');
      descripcionInput.value=row.getAttribute('data-descripcion')||'';
      estadoInput.value=row.getAttribute('data-estado');
      form.action='/ecografias/'+currentId+'/editar/';
      open(mEdit);
    });
  });
  
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(errorBox){ errorBox.style.display='none'; errorBox.textContent=''; }
      var fd=new FormData(form);
      fetch(form.getAttribute('action'),{ method:'POST', body:fd, credentials:'same-origin' })
        .then(function(res){
          if(res.status<400){
            close(mEdit);
            setTimeout(function(){ window.location.reload(); }, 600);
            return null;
          }
          return res.text();
        })
        .then(function(text){ if(text===null) return; if(errorBox){ errorBox.textContent='Error al guardar. Verifica los datos.'; errorBox.style.display='block'; } })
        .catch(function(){ if(errorBox){ errorBox.textContent='Error de conexión'; errorBox.style.display='block'; } });
    });
  }
});
