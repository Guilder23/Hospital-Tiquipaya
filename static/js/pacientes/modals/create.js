document.addEventListener('DOMContentLoaded',function(){
  var mCreate=document.getElementById('modal-crear-paciente');
  var btnOpenCreate=document.getElementById('btn-open-create');
  function open(m){m.setAttribute('aria-hidden','false')}
  function close(m){m.setAttribute('aria-hidden','true')}
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mCreate)close(mCreate)})})
  if(btnOpenCreate){btnOpenCreate.addEventListener('click',function(){open(mCreate)})}
});