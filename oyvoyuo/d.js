let input = document.getElementById('inputField');
let output = document.getElementById('outputField');
let btn = document.getElementById('sendButton');

btn.addEventListener("click", ()=> {
  output.value = input.value.substring(input.value.lenght - 1);
  log();
})

btn.addEventListener("click", log())

function log () {
  console.log(input.value);
}
