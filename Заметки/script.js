const taskBtn = document.getElementById("taskBtn");
const taskInput = document.getElementById("taskInput");

const saveTasks = () => {
    const tasks = [];
    document.querySelectorAll('.Note').forEach(note => {
        tasks.push({ text: note.querySelector('p').textContent });
    });
    localStorage.setItem("tasks", JSON.stringify(tasks));
};

const createTask = () => {
    if (taskInput.value !== "") {
        const newnote = document.createElement('div');
        newnote.classList.add('Note');

        const notetext = document.createElement('p');
        notetext.textContent = taskInput.value;

        const secondButton = document.createElement('button');
        secondButton.textContent = 'Удалить';

        newnote.appendChild(notetext);
        newnote.appendChild(secondButton);
        document.getElementById("To-Do-Container").appendChild(newnote);

        taskInput.value = '';

        secondButton.addEventListener('click', () => {
            newnote.remove();
            saveTasks();
        });

        saveTasks();
    } else {
        alert("Заполните все поля");
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const savedTasks = JSON.parse(localStorage.getItem("tasks")) || [];
    savedTasks.forEach(task => {
        const newnote = document.createElement('div');
        newnote.classList.add('Note');

        const notetext = document.createElement('p');
        notetext.textContent = task.text;

        const secondButton = document.createElement('button');
        secondButton.textContent = 'Удалить';

        newnote.appendChild(notetext);
        newnote.appendChild(secondButton);
        document.getElementById("To-Do-Container").appendChild(newnote);

        secondButton.addEventListener('click', () => {
            newnote.remove();
            saveTasks();
        });
    });
});

taskBtn.addEventListener("click", createTask);

taskInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        createTask();
    }
});
