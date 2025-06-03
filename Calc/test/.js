// Сохраняем элементы в переменные
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
const z = document.getElementById(",");
const ravno = document.getElementById("=");
const textField = document.getElementById("textField");
let txt = "";

// Добавляем обработчик события на кнопку
b1.addEventListener("click", () => {
    // Выводим текст в текстовое поле
    textField.value = textField.value + "1";
});