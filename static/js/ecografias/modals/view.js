document.addEventListener('DOMContentLoaded',function(){
  var mView=document.getElementById('modal-ver-ecografia');
  var codigoSpan=document.getElementById('view-codigo');
  var nombreSpan=document.getElementById('view-nombre');
  var medicoSpan=document.getElementById('view-medico');
  var especialidadSpan=document.getElementById('view-especialidad');
  var descripcionSpan=document.getElementById('view-descripcion');
  var estadoSpan=document.getElementById('view-estado');
  var fechaSpan=document.getElementById('view-fecha-creacion');
  
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mView)close(mView)})});
  
  document.querySelectorAll('.btn-view').forEach(function(btn){
    btn.addEventListener('click',function(){
      var row=this.closest('tr');
      codigoSpan.textContent=row.getAttribute('data-codigo');
      nombreSpan.textContent=row.getAttribute('data-nombre');
      var medicoId=row.getAttribute('data-medico_id');
      var medicoOpt=document.querySelector('#edit-medico option[value="'+medicoId+'"]');
      medicoSpan.textContent=medicoOpt?medicoOpt.textContent:'N/A';
      var especialidadId=row.getAttribute('data-especialidad_id');
      var especialidadOpt=document.querySelector('#edit-especialidad option[value="'+especialidadId+'"]');
      especialidadSpan.textContent=especialidadOpt?especialidadOpt.textContent:'N/A';
      descripcionSpan.textContent=row.getAttribute('data-descripcion')||'(Sin descripción)';
      var estado=row.getAttribute('data-estado');
      estadoSpan.innerHTML=estado==='ACTIVA'?'<span class="badge badge-activo">Activa</span>':'<span class="badge badge-inactivo">Inactiva</span>';
      fechaSpan.textContent=row.getAttribute('data-fecha_creacion');
      open(mView);
    });
  });
});
