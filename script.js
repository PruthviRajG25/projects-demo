{/* <script> */}
        let todos = [];

        const input = document.getElementById('todo-input');
        const addBtn = document.getElementById('add-btn');
        const list = document.getElementById('todo-list');
        const prioritySelect = document.getElementById('priority');
        const filterSelect = document.getElementById('filter');
        const clearCompletedBtn = document.getElementById('clear-completed');
        const totalCount = document.getElementById('total-count');
        const activeCount = document.getElementById('active-count');
        const completedCount = document.getElementById('completed-count');

        function sanitizeText(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function updateStats() {
            totalCount.textContent = todos.length;
            activeCount.textContent = todos.filter(t => !t.completed).length;
            completedCount.textContent = todos.filter(t => t.completed).length;
        }

        function createToDoNode(todo) {
            const li = document.createElement('li');
            li.className = `todo-item priority-${todo.priority}`;

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'todo-checkbox';
            checkbox.checked = todo.completed;
            checkbox.addEventListener('change', () => {
                todo.completed = checkbox.checked;
                textSpan.className = `todo-text${todo.completed ? ' completed' : ''}`;
                updateStats();
            });

            const textSpan = document.createElement('span');
            textSpan.className = `todo-text${todo.completed ? ' completed' : ''}`;
            textSpan.innerHTML = sanitizeText(todo.text);
            textSpan.title = 'Double-click to edit';

            textSpan.addEventListener('dblclick', () => {
                const newText = prompt('Edit your todo:', todo.text);
                if (newText !== null && newText.trim()) {
                    todo.text = newText.trim();
                    textSpan.innerHTML = sanitizeText(todo.text);
                }
            });

            const priorityBadge = document.createElement('span');
            priorityBadge.className = `priority-badge ${todo.priority}`;
            priorityBadge.textContent = todo.priority;

            const dateSpan = document.createElement('span');
            dateSpan.className = 'todo-date';
            const date = new Date(todo.date);
            dateSpan.textContent = date.toLocaleDateString();
            dateSpan.title = date.toLocaleString();

            const delBtn = document.createElement('button');
            delBtn.className = 'delete-btn';
            delBtn.innerHTML = '×';
            delBtn.addEventListener('click', () => {
                todos = todos.filter(t => t.id !== todo.id);
                render();
            });

            li.appendChild(checkbox);
            li.appendChild(textSpan);
            li.appendChild(priorityBadge);
            li.appendChild(dateSpan);
            li.appendChild(delBtn);
            return li;
        }

        function render() {
            list.innerHTML = '';
            updateStats();

            const filter = filterSelect.value;
            const filteredTodos = todos.filter(todo => {
                if (filter === 'all') return true;
                return filter === 'completed' ? todo.completed : !todo.completed;
            });

            if (filteredTodos.length === 0) {
                const emptyState = document.createElement('div');
                emptyState.className = 'empty-state';
                emptyState.innerHTML = `
                    <div class="empty-state-icon">📝</div>
                    <div class="empty-state-text">No tasks ${filter === 'all' ? 'yet' : filter}</div>
                    <div class="empty-state-subtext">${filter === 'all' ? 'Add a task to get started!' : ''}</div>
                `;
                list.appendChild(emptyState);
                return;
            }

            filteredTodos.forEach(todo => {
                const node = createToDoNode(todo);
                if (node) list.appendChild(node);
            });
        }

        function addToDo() {
            const text = input.value.trim();
            const priority = prioritySelect.value;

            if (!text) {
                input.focus();
                return;
            }

            if (text.length > 100) {
                alert('Todo text is too long! Maximum 100 characters.');
                return;
            }

            todos.push({
                text,
                completed: false,
                priority,
                date: new Date().toISOString(),
                id: Date.now()
            });

            input.value = '';
            input.focus();
            render();
        }

        function clearCompleted() {
            const completedTodos = todos.filter(t => t.completed);
            if (completedTodos.length === 0) {
                alert('No completed tasks to clear!');
                return;
            }
            
            if (confirm(`Clear ${completedTodos.length} completed task(s)?`)) {
                todos = todos.filter(todo => !todo.completed);
                render();
            }
        }

        input.addEventListener('keypress', e => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addToDo();
            }
        });

        addBtn.addEventListener('click', addToDo);
        filterSelect.addEventListener('change', render);
        clearCompletedBtn.addEventListener('click', clearCompleted);

        // Initial render
        render();
        input.focus();
    {/* </script> */}