<script setup lang="ts">
import { ref } from 'vue'

interface Note {
  id: string
  content: string
}

const notes = ref<Note[]>([]);
const newNote = ref('');

const showConfirm = ref(false);
const noteToDelete = ref<string | null>(null);

function addNote() {
  if (!newNote.value.trim()) return;
  notes.value.push({ id: Date.now().toString(), content: newNote.value.trim() });
  newNote.value = '';
  saveNotes();
}

function askRemoveNote(id: string) {
  noteToDelete.value = id;
  showConfirm.value = true;
}

function confirmRemove() {
  if (noteToDelete.value) {
    notes.value = notes.value.filter(n => n.id !== noteToDelete.value);
    saveNotes();
  }
  closeConfirm();
}

function closeConfirm() {
  showConfirm.value = false;
  noteToDelete.value = null;
}

function saveNotes() {
  localStorage.setItem('notes', JSON.stringify(notes.value));
}

function loadNotes() {
  const saved = localStorage.getItem('notes');
  if (saved) {
    notes.value = JSON.parse(saved);
  }
}

loadNotes();
</script>

<template>
  <div class="Router"><router-link to="/DateFlower" class="nav-link">Вернуться к датам</router-link></div>
  
  <section class="notes-container">
    <h2>Любовные записки ❤️</h2>

    <div class="input-row">
      <textarea
        v-model="newNote"
        placeholder="Напиши что-нибудь милое..."
        rows="3"
      ></textarea>
      <button @click="addNote" :disabled="!newNote.trim()">Добавить</button>
    </div>

    <ul class="notes-list" v-if="notes.length">
      <li v-for="note in notes" :key="note.id" class="note-item">
        <p>{{ note.content }}</p>
        <button class="btn-delete" @click="askRemoveNote(note.id)">Удалить</button>
      </li>
    </ul>

    <p v-else class="empty-msg">Пока нет записок. Напиши первую ❤️</p>

    <div v-if="showConfirm" class="confirm-overlay" @click.self="closeConfirm">
      <div class="confirm-dialog">
        <p>Ты точно хочешь удалить эту записку?</p>
        <div class="confirm-buttons">
          <button class="btn btn-cancel" @click="closeConfirm">Отмена</button>
          <button class="btn btn-confirm" @click="confirmRemove">Удалить</button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.notes-container {
  max-width: 480px;
  margin: 2rem auto;
  padding: 1.5rem 2rem;
  background: #121218;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(77, 171, 247, 0.4);
  color: #e0e0e0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 1rem;
  color: #4dabf7;
  font-weight: 700;
}

.input-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

textarea {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: none;
  resize: vertical;
  font-size: 1rem;
  font-family: inherit;
  background: #22222a;
  color: #e0e0e0;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);
  transition: background-color 0.3s ease;
}

textarea:focus {
  outline: none;
  background: #2c2c39;
  box-shadow: 0 0 8px #4dabf7;
}

button {
  background: #4dabf7;
  border: none;
  color: white;
  font-weight: 700;
  padding: 0 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  user-select: none;
}

button:disabled {
  background: #6ea6f9aa;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background: #3391ff;
}

.notes-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 400px;
  overflow-y: auto;
}

.note-item {
  background: #1f1f29;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  margin-bottom: 0.9rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 0 8px rgba(77, 171, 247, 0.1);
  transition: background-color 0.3s ease;
}

.note-item p {
  margin: 0;
  flex: 1;
  padding-right: 1rem;
  word-break: break-word;
  font-size: 1rem;
  line-height: 1.3;
  color: #b0c7ff;
}

.btn-delete {
  background: #e57373;
  padding: 0.3rem 0.7rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
  user-select: none;
}

.btn-delete:hover {
  background: #d33b3b;
}

.empty-msg {
  text-align: center;
  color: #777a85;
  font-style: italic;
  margin-top: 2rem;
}

/* Модальное окно подтверждения */

.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(18, 18, 24, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.confirm-dialog {
  background: #22222a;
  padding: 2rem;
  border-radius: 16px;
  max-width: 320px;
  box-shadow: 0 0 15px #4dabf7;
  text-align: center;
  color: #e0e0e0;
}

.confirm-dialog p {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #f44336;
}

.confirm-buttons {
  display: flex;
  justify-content: space-around;
}

.btn {
  min-width: 100px;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s ease;
}

.btn-cancel {
  background: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background: #565e64;
}

.btn-confirm {
  background: #f44336;
  color: white;
}

.btn-confirm:hover {
  background: #d32f2f;
}
.Router {
  display: flex;
  text-align: center;
  justify-content: center;
  align-items: center;
}
.nav-link {
  display: inline-block;
  margin-bottom: 1.5rem;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(145deg, #4dabf7, #1e90ff);
  box-shadow: 0 0 10px rgba(77, 171, 247, 0.6), 0 0 5px rgba(77, 171, 247, 0.3);
  text-decoration: none;
  transition: all 0.3s ease;
}
.nav-link:hover {
  background: linear-gradient(145deg, #63b3ff, #3598ff);
  box-shadow: 0 0 15px rgba(77, 171, 247, 0.8), 0 0 10px rgba(77, 171, 247, 0.4);
  transform: translateY(-2px);
}
</style>
