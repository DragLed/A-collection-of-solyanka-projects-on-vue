document.addEventListener('DOMContentLoaded', function() {

const box = document.getElementById('box');
const increaseButton = document.getElementById('plus');
const decreaseButton = document.getElementById('minus');
const resetButton = document.getElementById('reset');

const initialWidth = 100;
const initialHeight = 100;
const step = 50;

increaseButton.addEventListener('click', function() {
  box.style.width = `${box.offsetWidth + step}px`;
  box.style.height = `${box.offsetHeight + step}px`;
});

decreaseButton.addEventListener('click', function() {
  box.style.width = `${box.offsetWidth - step}px`;
  box.style.height = `${box.offsetHeight - step}px`;
});

resetButton.addEventListener('click', function() {
  box.style.width = `${initialWidth}px`;
  box.style.height = `${initialHeight}px`;
});
});
