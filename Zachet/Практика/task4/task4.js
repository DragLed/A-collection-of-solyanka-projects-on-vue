document.addEventListener('DOMContentLoaded', function() {
  let masyunya = document.getElementById('masyunya');
  let box = document.getElementById('box');

  box.addEventListener('mouseover', function () {
    box.style.backgroundColor = "black";
    masyunya.style.visibility = "visible";
  })
  box.addEventListener('mouseout', function () {
    box.style.backgroundColor = "wheat";
    masyunya.style.visibility = "hidden";
  })



});
