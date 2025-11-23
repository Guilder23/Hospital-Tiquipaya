document.addEventListener('DOMContentLoaded',function(){
  function getCookie(name){ var v=document.cookie.match('(^|;)\\s*'+name+'\\s*=\\s*([^;]+)'); return v? v.pop():''; }
  var modalValidar=document.getElementById('modal-validar');
  var btnValidar=document.getElementById('btn-validar');
  var valError=document.getElementById('val-error');
  function closeModal(m){ if(!m) return; m.classList.remove('is-open'); m.setAttribute('aria-hidden','true'); m.style.display='none'; }
  function openModal(m){ if(!m) return; m.classList.add('is-open'); m.setAttribute('aria-hidden','false'); m.style.display='flex'; }
  if(modalValidar){ openModal(modalValidar); }
  if(btnValidar){ btnValidar.addEventListener('click',function(){
    var ci=document.getElementById('val-ci').value.trim();
    var fn=document.getElementById('val-fn').value.trim();
    fetch('/citas/validar/',{ method:'POST', headers:{ 'Content-Type':'application/x-www-form-urlencoded','X-CSRFToken':getCookie('csrftoken') }, body:'ci='+encodeURIComponent(ci)+'&fecha_nacimiento='+encodeURIComponent(fn) })
      .then(function(r){ return r.json(); })
      .then(function(data){ if(!data.ok){ if(valError){ valError.textContent=data.error||'Error'; valError.style.display='block'; } return; } window.location.href=data.redirect; })
      .catch(function(){ if(valError){ valError.textContent='Error de conexión'; valError.style.display='block'; } });
  }); }
  document.querySelectorAll('.btn-horarios').forEach(function(btn){ btn.addEventListener('click',function(){
    var id=btn.getAttribute('data-id');
    fetch('/citas/agenda/'+id+'/')
      .then(function(r){ return r.json(); })
      .then(function(data){ var cont=document.getElementById('slots-'+id); if(!cont) return; cont.innerHTML=''; ['mannana','tarde'].forEach(function(turno){ var lista=data.turnos[turno]||[]; lista.forEach(function(s){ var d=document.createElement('div'); d.className='slot '+(s.ocupado?'busy':'free'); d.textContent=s.hora; d.setAttribute('data-hora',s.hora); d.setAttribute('data-medico',id); if(!s.ocupado){ d.addEventListener('click',onSelectSlot); } cont.appendChild(d); }); }); document.getElementById('conf-fecha').textContent=data.fecha; });
  }); });
  var modalConfirm=document.getElementById('modal-confirm');
  var btnConfCancel=document.getElementById('btn-conf-cancel');
  var btnConfOk=document.getElementById('btn-conf-ok');
  var confError=document.getElementById('conf-error');
  var selected={ medico:null, hora:null, esp:null, medicoNombre:null };
  function onSelectSlot(e){ var el=e.currentTarget; selected.medico=el.getAttribute('data-medico'); selected.hora=el.getAttribute('data-hora'); var card=document.querySelector('.doctor-card[data-id="'+selected.medico+'"]'); if(card){ var info=card.querySelector('.doctor-info'); var lines=info ? info.querySelectorAll('div') : []; selected.medicoNombre=lines[0]?lines[0].textContent:''; selected.esp=lines[1]?lines[1].textContent.split(' · ')[0]:''; }
    document.getElementById('conf-medico').textContent=selected.medicoNombre||'';
    document.getElementById('conf-esp').textContent=selected.esp||'';
    document.getElementById('conf-hora').textContent=selected.hora||'';
    var fecha=document.getElementById('conf-fecha').textContent||'';
    document.getElementById('conf-resumen').textContent=(selected.medicoNombre||'')+' · '+(selected.esp||'')+' · '+fecha+' '+selected.hora;
    openModal(modalConfirm);
  }
  if(btnConfCancel){ btnConfCancel.addEventListener('click',function(){ closeModal(modalConfirm); }); }
  if(btnConfOk){ btnConfOk.addEventListener('click',function(){ confError.style.display='none'; confError.textContent='';
    var fd=new URLSearchParams(); fd.append('medico_id',selected.medico); fd.append('hora',selected.hora);
    fetch('/citas/confirmar/',{ method:'POST', headers:{ 'Content-Type':'application/x-www-form-urlencoded','X-CSRFToken':getCookie('csrftoken') }, body:fd.toString() })
  
      .then(function(r){ return r.json(); })
      .then(function(data){ if(!data.ok){ confError.textContent=data.error||'Error'; confError.style.display='block'; return; }
        closeModal(modalConfirm);
        var cont=document.getElementById('slots-'+selected.medico); if(cont){ cont.querySelectorAll('.slot.free').forEach(function(s){ if(s.getAttribute('data-hora')===selected.hora){ s.classList.remove('free'); s.classList.add('busy'); } }); }
        window.location.href='/citas/orden/'+data.cita_id+'/';
      })
      .catch(function(){ confError.textContent='Error de conexión'; confError.style.display='block'; });
  }); }
});

