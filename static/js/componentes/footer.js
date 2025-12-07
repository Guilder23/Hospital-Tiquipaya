document.addEventListener('DOMContentLoaded', function(){
  var footers = document.querySelectorAll('.site-footer');
  if(footers.length > 1){
    for(var i=0;i<footers.length-1;i++){
      footers[i].remove();
    }
  }
});
