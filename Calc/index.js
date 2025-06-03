const AC = document.getElementById("AC");
const procent = document.getElementById("%");
const backspace = document.getElementById("backspace");
const delenie = document.getElementById("/");
const b7 = document.getElementById("7");
const b8 = document.getElementById("8");
const b9 = document.getElementById("9");
const ymnozhenie = document.getElementById("*");
const b4 = document.getElementById("4");
const b5 = document.getElementById("5");
const b6 = document.getElementById("6");
const vichitanie = document.getElementById("-");
const b1 = document.getElementById("1");
const b2 = document.getElementById("2");
const b3 = document.getElementById("3");
const slozhenie = document.getElementById("+");
const b00 = document.getElementById("00");
const b0 = document.getElementById("0");
const z = document.getElementById(".");
const ravno = document.getElementById("=");
const textField = document.getElementById("TextField");
let znak = "";


b1.addEventListener("click", () => {textField.value = textField.value + "1"});
b2.addEventListener("click", () => {textField.value = textField.value + "2"});
b3.addEventListener("click", () => {textField.value = textField.value + "3"});
b4.addEventListener("click", () => {textField.value = textField.value + "4"});
b5.addEventListener("click", () => {textField.value = textField.value + "5"});
b6.addEventListener("click", () => {textField.value = textField.value + "6"});
b7.addEventListener("click", () => {textField.value = textField.value + "7"});
b8.addEventListener("click", () => {textField.value = textField.value + "8"});
b9.addEventListener("click", () => {textField.value = textField.value + "9"});
b0.addEventListener("click", () => {textField.value = textField.value + "0"});
b00.addEventListener("click", () => {textField.value = textField.value + "00"});
AC.addEventListener("click", () => {textField.value = ""});
procent.addEventListener("click", () => {textField.value = textField.value + "%"});
delenie.addEventListener("click", () => {textField.value = textField.value + "÷";
    znak = "/";
});
//backspace.addEventListener("click", () => {textField.value = textField.value + ""});
ymnozhenie.addEventListener("click", () => {textField.value = textField.value + "*";
    znak = "*";});
slozhenie.addEventListener("click", () => {textField.value = textField.value + "+";
    znak = "+";});
z.addEventListener("click", () => {textField.value = textField.value + "."});
vichitanie.addEventListener("click", () => {textField.value = textField.value + "-";
    znak = "-";});

function chet(znak){
    if (znak == "/"){
        let a = textField.value.split("÷");
        console.log(a)
        textField.value = a[0] / a[1];
        console.log(textField.value)
    }
    else if (znak == "-") {
        let a = textField.value.split("-");
        console.log(a)
        textField.value = a[0] - a[1];
        console.log(textField.value)
    }
    else if (znak == "*") {
        let a = textField.value.split("*");
        console.log(a)
        textField.value = a[0] * a[1];
        console.log(textField.value)
    }
    else if (znak == "+") {
        let a = textField.value.split("+");
        
        textField.value = parseInt(a[0]) + parseInt(a[1]);
        console.log(textField.value)
    }
    else {textField.value = textField.value}

    
}

ravno.addEventListener("click", () => {chet(znak)});



