document.addEventListener('DOMContentLoaded', function() {
  const box = document.getElementById('container');

box.addEventListener('click', function(){
  if (box.style.justifyContent == 'flex-start'){
   box.style.justifyContent = 'flex-end';
  }
  else {
    box.style.justifyContent = 'flex-start';
  }
  console.log("D");
});
});
