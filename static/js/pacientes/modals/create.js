document.addEventListener('DOMContentLoaded',function(){
  var mCreate=document.getElementById('modal-crear-paciente');
  var btnOpenCreate=document.getElementById('btn-open-create');
  var form=document.getElementById('form-create');
  var errorBox=document.getElementById('create-error');
  function open(m){ if(!m) return; m.style.display='flex'; m.setAttribute('aria-hidden','false'); }
  function close(m){ if(!m) return; m.style.display='none'; m.setAttribute('aria-hidden','true'); }
  document.querySelectorAll('[data-close]').forEach(function(el){el.addEventListener('click',function(){if(mCreate)close(mCreate)})})
  if(btnOpenCreate){btnOpenCreate.addEventListener('click',function(){open(mCreate)})}
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(errorBox){ errorBox.style.display='none'; errorBox.textContent=''; }
      var ci=form.querySelector('[name="ci"]');
      var nombres=form.querySelector('[name="nombres"]');
      var apellido_paterno=form.querySelector('[name="apellido_paterno"]');
      var email=form.querySelector('[name="email"]');
      var valid=true;
      if(!ci || !ci.value.trim()){ valid=false; }
      if(!nombres || !nombres.value.trim()){ valid=false; }
      if(!apellido_paterno || !apellido_paterno.value.trim()){ valid=false; }
      if(email && email.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)){ valid=false; }
      if(!valid){ if(errorBox){ errorBox.textContent='Revisa los campos requeridos'; errorBox.style.display='block'; } return; }
      var fd=new FormData(form);
      var tsEl=form.querySelector('[name="tiene_seguro"]');
      if(tsEl){
        var tsVal=tsEl.value;
        fd.delete('tiene_seguro');
        if(tsVal==='True'){ fd.append('tiene_seguro','on'); }
      }
      fetch(form.getAttribute('action'),{ method:'POST', body:fd, credentials:'same-origin' })
        .then(function(res){
          if(res.redirected){
            try{ localStorage.setItem('toast_message','Paciente creado'); localStorage.setItem('toast_type','success'); }catch(e){}
            close(mCreate);
            setTimeout(function(){ window.location.href=res.url||'/pacientes/'; }, 800);
            return null;
          }
          return res.text();
        })
        .then(function(text){ if(text===null) return; if(errorBox){ errorBox.textContent='No se pudo guardar. Revisa los campos.'; errorBox.style.display='block'; } })
        .catch(function(){ if(errorBox){ errorBox.textContent='Error de conexión'; errorBox.style.display='block'; } });
    });
  }
});