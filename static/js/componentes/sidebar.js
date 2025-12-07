document.addEventListener('DOMContentLoaded', function(){
  var sidebar = document.querySelector('.sidebar');
  var btn = document.getElementById('sidebar-toggle');
  if(!sidebar || !btn) return;
  function ensureOverlay(){
    var o = document.querySelector('.sidebar-overlay');
    if(!o){
      o = document.createElement('div');
      o.className = 'sidebar-overlay';
      document.body.appendChild(o);
    }
    return o;
  }
  function open(){
    document.body.classList.add('sidebar-open');
    var o = ensureOverlay();
    o.style.display = 'block';
  }
  function close(){
    document.body.classList.remove('sidebar-open');
    var o = document.querySelector('.sidebar-overlay');
    if(o){ o.style.display = 'none'; }
  }
  btn.addEventListener('click', function(){
    if(document.body.classList.contains('sidebar-open')){ close(); } else { open(); }
  });
  document.addEventListener('click', function(e){
    var o = document.querySelector('.sidebar-overlay');
    if(o && e.target === o){ close(); }
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') close(); });
  function handleResize(){ if(window.innerWidth > 992) close(); }
  window.addEventListener('resize', handleResize);
});
