// Получаем первую кнопку по ID
const firstButton = document.getElementById('firstButton');

// Обработчик события для первой кнопки
firstButton.addEventListener('click', () => {
    // Создаем div, в котором будет текст и кнопка
    const newDiv = document.createElement('div');

    // Создаем текстовый элемент
    const newText = document.createElement('p');
    newText.textContent = 'Это новый текст в div!';

    // Создаем вторую кнопку
    const secondButton = document.createElement('button');
    secondButton.textContent = 'Удалить этот div';

    // Добавляем текст и кнопку в новый div
    newDiv.appendChild(newText);
    newDiv.appendChild(secondButton);

    // Добавляем новый div на страницу
    document.body.appendChild(newDiv);

    // Обработчик события для второй кнопки (удаляет div)
    secondButton.addEventListener('click', () => {
        newDiv.remove(); // Удаляем div
    });
});
