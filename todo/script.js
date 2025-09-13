document.addEventListener('DOMContentLoaded', () => {
    const todoInput = document.getElementById('todo-input');
    const addBtn = document.getElementById('add-btn');
    const todoList = document.getElementById('todo-list');

    loadTodos();

    addBtn.addEventListener('click', addTodo);
    todoList.addEventListener('click', handleTodoClick);
    todoInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTodo();
        }
    });

    function addTodo() {
        const todoText = todoInput.value.trim();
        if (todoText === '') {
            return;
        }

        const todoItem = createTodoItem(todoText);
        todoList.appendChild(todoItem);
        saveTodos();
        todoInput.value = '';
    }

    function createTodoItem(text, completed = false) {
        const li = document.createElement('li');
        li.className = 'todo-item';
        if (completed) {
            li.classList.add('completed');
        }

        const span = document.createElement('span');
        span.textContent = text;

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = 'Delete';

        li.appendChild(span);
        li.appendChild(deleteBtn);

        return li;
    }

    function handleTodoClick(e) {
        if (e.target.classList.contains('delete-btn')) {
            const todoItem = e.target.parentElement;
            todoList.removeChild(todoItem);
            saveTodos();
        } else if (e.target.tagName === 'SPAN' || e.target.tagName === 'LI') {
            const todoItem = e.target.closest('.todo-item');
            todoItem.classList.toggle('completed');
            saveTodos();
        }
    }

    function saveTodos() {
        const todos = [];
        document.querySelectorAll('.todo-item').forEach(item => {
            todos.push({
                text: item.querySelector('span').textContent,
                completed: item.classList.contains('completed')
            });
        });
        localStorage.setItem('todos', JSON.stringify(todos));
    }

    function loadTodos() {
        const todos = JSON.parse(localStorage.getItem('todos'));
        if (todos) {
            todos.forEach(todo => {
                const todoItem = createTodoItem(todo.text, todo.completed);
                todoList.appendChild(todoItem);
            });
        }
    }
});
