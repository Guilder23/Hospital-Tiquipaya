document.addEventListener('DOMContentLoaded',function(){
  var mCreate=document.getElementById('modal-crear-ecografia');
  var btnOpenCreate=document.getElementById('btn-open-create');
  var form=document.getElementById('form-create');
  var errorBox=document.getElementById('create-error');
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mCreate)close(mCreate)})});
  if(btnOpenCreate){btnOpenCreate.addEventListener('click',function(){open(mCreate)})}
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(errorBox){ errorBox.style.display='none'; errorBox.textContent=''; }
      var fd=new FormData(form);
      fd.append('X-Requested-With', 'XMLHttpRequest');
      fetch(form.getAttribute('action'),{ method:'POST', body:fd, credentials:'same-origin', headers:{'X-Requested-With':'XMLHttpRequest'} })
        .then(function(res){
          if(res.status<400){
            return res.json().then(function(data){
              if(data.success){
                close(mCreate);
                if(typeof showNotification === 'function'){
                  showNotification(data.message, 'success');
                }
                setTimeout(function(){ window.location.href = data.redirect; }, 1500);
              }
              return null;
            }).catch(function(){
              close(mCreate);
              setTimeout(function(){ window.location.reload(); }, 600);
              return null;
            });
          }
          return res.text();
        })
        .then(function(text){ if(text===null) return; if(errorBox){ errorBox.textContent='Error al guardar. Verifica los datos.'; errorBox.style.display='block'; } })
        .catch(function(){ if(errorBox){ errorBox.textContent='Error de conexión'; errorBox.style.display='block'; } });
    });
  }
});
