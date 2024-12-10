function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (response) {
        return response.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
    
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');
            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');
        
            tdTitle.innerText = films[i].title == films[i].title_ru ? '' : films[i].title;
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;
        
            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';
            editButton.onclick = function() {
                editFilm(i);
            };
        
            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru); // Исправлено: передаем индекс i вместо films[i].id
            };
        
            tdActions.append(editButton);
            tdActions.append(delButton);
        
            tr.append(tdTitle);
            tr.append(tdTitleRus);
            tr.append(tdYear);
            tr.append(tdActions);
        
            tbody.append(tr);
        }
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function (response) {
        if (response.status === 204) {
            fillFilmList(); // Обновляем список фильмов
        } else {
            alert('Ошибка при удалении фильма');
        }
    })
    .catch(function (error) {
        console.error('Ошибка при удалении фильма:', error);
        alert('Не удалось удалить фильм. Пожалуйста, попробуйте позже.');
    });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    showModal();
}

document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();

    function addFilm() {
        const idElement = document.getElementById('id');
        const titleElement = document.getElementById('title');
        const titleRuElement = document.getElementById('title-ru');
        const yearElement = document.getElementById('year');
        const descriptionElement = document.getElementById('description');

        if (idElement) idElement.value = '';
        if (titleElement) titleElement.value = '';
        if (titleRuElement) titleRuElement.value = '';
        if (yearElement) yearElement.value = '';
        if (descriptionElement) descriptionElement.value = '';

        showModal();
    }

    document.getElementById('add-film-button').addEventListener('click', addFilm);
});

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(function() {
        fillFilmList();
        hideModal();
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function(response) {
        return response.json();
    })
    .then(function(film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    });
}
