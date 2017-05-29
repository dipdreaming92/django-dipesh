window.addEventListener('load', handleLoad);

function handleLoad() {
    var form = document.querySelector('.todo-form form');
    var messages = document.querySelector('.messages');
    var checkboxes = document.querySelectorAll('.todo-complete-check');

    if (checkboxes) {
        // Register check event handler for each checkbox
        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].addEventListener('change', handleTodoCheckChange);
        }
    }

    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }

    if (messages) {
        console.log('Message will be hidden after 5 seconds.');
        setTimeout(hideMessages, 5000);
    }
}

function HideMessages() {
    //var messages=document.querySelector('.messages');

    //messages.style.display='none';
    $('.messages').fadeOut();
}

function handleFormSubmit(e) {
    var titleInput = document.querySelector('#input-todo-title');
    var title = titleInput.value.trim();

    if (!title || title === '') {
        alert('Please enter the title.');
        titleInput.focus();
        e.preventDefault();
    }
}
function handleTodoCheckChange(e) {
    var checked = e.target.checked;
    var todoId = e.target.getAttribute('data-id');
    var body = {'completed': checked};

    console.log('todo: ', todoId, checked);

    // Do a PATCH request with the completed data.
    console.log('Sending a PATCH request');

    axios.patch('/api/todos/' + todoId, body)
        .then(function(response) {
            console.log('Response received', response.statusText, response.data);
        });
}