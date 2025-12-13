document.addEventListener('DOMContentLoaded', function(){
  var nav = document.querySelector('.site-header nav');
  var btn = document.getElementById('nav-toggle');
  if(!nav || !btn) return;
  function ensureOverlay(){
    var o = document.querySelector('.nav-overlay');
    if(!o){
      o = document.createElement('div');
      o.className = 'nav-overlay';
      document.body.appendChild(o);
    }
    return o;
  }
  function open(){ document.body.classList.add('nav-open'); ensureOverlay(); }
  function close(){
    document.body.classList.remove('nav-open');
    var o = document.querySelector('.nav-overlay');
    if(o){ o.remove(); }
  }
  btn.addEventListener('click', function(){
    if(document.body.classList.contains('nav-open')) close(); else open();
  });
  document.addEventListener('click', function(e){ var o=document.querySelector('.nav-overlay'); if(o && e.target===o) close(); });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') close(); });
  function handleResize(){ if(window.innerWidth>992) close(); }
  window.addEventListener('resize', handleResize);
});
