document.addEventListener('DOMContentLoaded', function(){
  function createToast(message, type){
    var container = document.querySelector('.toast-container');
    if(!container){
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    var toast = document.createElement('div');
    toast.className = 'toast ' + (type||'info');
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(function(){ toast.classList.add('show'); }, 10);
    setTimeout(function(){ toast.classList.remove('show'); toast.addEventListener('transitionend', function(){ toast.remove(); }); }, 3000);
  }
  window.showToast = createToast;
  try{
    var saved = localStorage.getItem('toast_message');
    var savedType = localStorage.getItem('toast_type');
    if(saved){
      createToast(saved, savedType||'success');
      localStorage.removeItem('toast_message');
      localStorage.removeItem('toast_type');
    }
  }catch(e){}
});