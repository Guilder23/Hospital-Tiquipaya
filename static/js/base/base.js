document.addEventListener('DOMContentLoaded', function(){
  // Sistema antiguo de toasts - desactivado en favor del nuevo sistema de notifications
  // function createToast(message, type){
  //   var container = document.querySelector('.toast-container');
  //   if(!container){
  //     container = document.createElement('div');
  //     container.className = 'toast-container';
  //     document.body.appendChild(container);
  //   }
  //   var toast = document.createElement('div');
  //   toast.className = 'toast ' + (type||'info');
  //   toast.textContent = message;
  //   container.appendChild(toast);
  //   setTimeout(function(){ toast.classList.add('show'); }, 10);
  //   setTimeout(function(){ toast.classList.remove('show'); toast.addEventListener('transitionend', function(){ toast.remove(); }); }, 3000);
  // }
  // window.showToast = createToast;
  
  // Sistema nuevo de notifications mediante Django messages
  // Ver: static/js/componentes/notifications.js y templates/componentes/messages.html
  
  try{
    var saved = localStorage.getItem('toast_message');
    var savedType = localStorage.getItem('toast_type');
    if(saved){
      // Usar el nuevo sistema
      if(typeof showNotification === 'function'){
        showNotification(saved, savedType||'success');
      }
      localStorage.removeItem('toast_message');
      localStorage.removeItem('toast_type');
    }
  }catch(e){}
  var tables = document.querySelectorAll('table');
  tables.forEach(function(t){
    if(!t.closest('.table-responsive')){
      var wrap = document.createElement('div');
      wrap.className = 'table-responsive';
      t.parentNode.insertBefore(wrap, t);
      wrap.appendChild(t);
    }
  });
});

