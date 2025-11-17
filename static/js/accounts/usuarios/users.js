document.addEventListener('DOMContentLoaded',function(){
  var modalCreate=document.getElementById('modal-crear-usuario');
  var modalEdit=document.getElementById('modal-editar-usuario');
  var modalDelete=document.getElementById('modal-eliminar-usuario');
  var modalView=document.getElementById('modal-ver-usuario');
  var btnOpenCreate=document.getElementById('btn-open-create');
  function open(modal){modal.setAttribute('aria-hidden','false')}
  function close(modal){modal.setAttribute('aria-hidden','true')}
  document.querySelectorAll('[data-close]').forEach(function(el){
    el.addEventListener('click',function(){
      [modalCreate,modalEdit,modalDelete,modalView].forEach(function(m){if(m)close(m)});
    })
  })
  if(btnOpenCreate){btnOpenCreate.addEventListener('click',function(){open(modalCreate)})}
  document.querySelectorAll('.btn-edit').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var row=document.querySelector('tr[data-id="'+id+'"]');
      var form=document.getElementById('form-edit');
      form.setAttribute('action','/accounts/usuarios/'+id+'/editar/');
      form.querySelector('[name="username"]').value=row.getAttribute('data-username')||'';
      form.querySelector('[name="first_name"]').value=row.getAttribute('data-first_name')||'';
      form.querySelector('[name="last_name"]').value=row.getAttribute('data-last_name')||'';
      form.querySelector('[name="email"]').value=row.getAttribute('data-email')||'';
      var active=row.getAttribute('data-active');
      var activeSel=form.querySelector('[name="is_active"]');
      if(activeSel){activeSel.value=(active==='True'?'True':'False')}
      var tipoId=row.getAttribute('data-tipo_id')||'';
      var tipoSel=form.querySelector('[name="tipo"]');
      if(tipoSel){tipoSel.value=tipoId}
      open(modalEdit);
    })
  })
  document.querySelectorAll('.btn-delete').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var username=btn.getAttribute('data-username');
      var form=document.getElementById('form-delete');
      form.setAttribute('action','/accounts/usuarios/'+id+'/eliminar/');
      var txt=document.getElementById('delete-text');
      if(txt){txt.textContent='¿Confirmas eliminar "'+username+'"?'}
      open(modalDelete);
    })
  })
  document.querySelectorAll('.btn-view').forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-id');
      var row=document.querySelector('tr[data-id="'+id+'"]');
      var u=row.getAttribute('data-username')||'';
      var fn=row.getAttribute('data-first_name')||'';
      var ln=row.getAttribute('data-last_name')||'';
      var em=row.getAttribute('data-email')||'';
      var act=row.getAttribute('data-active')==='True'?'Sí':'No';
      var rol=row.getAttribute('data-tipo_nombre')||'Sin rol';
      var elU=document.getElementById('view-username'); if(elU)elU.textContent=u;
      var elN=document.getElementById('view-name'); if(elN)elN.textContent=(fn+' '+ln).trim();
      var elE=document.getElementById('view-email'); if(elE)elE.textContent=em;
      var elA=document.getElementById('view-active'); if(elA)elA.textContent=act;
      var elR=document.getElementById('view-rol'); if(elR)elR.textContent=rol;
      open(modalView);
    })
  })
});