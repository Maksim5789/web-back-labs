function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (response) {
            return response.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = ''; // Очищаем таблицу

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                // Название на русском
                let tdRussianTitle = document.createElement('td');
                tdRussianTitle.innerText = films[i].title_ru || '';

                // Название на оригинальном языке (курсивом и в скобках)
                let tdOriginalTitle = document.createElement('td');
                if (films[i].title) {
                    tdOriginalTitle.innerHTML = `<i>(${films[i].title})</i>`;
                } else {
                    tdOriginalTitle.innerText = ''; // Если оригинальное название отсутствует, оставляем пустое поле
                }

                // Год выпуска
                let tdYear = document.createElement('td');
                tdYear.innerText = films[i].year || '';

                // Действия (кнопки "Редактировать" и "Удалить")
                let tdActions = document.createElement('td');

                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                editButton.onclick = function () {
                    editFilm(i);
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = function () {
                    deleteFilm(i, films[i].title_ru); // Передаем индекс i и название фильма
                };

                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавляем ячейки в строку
                tr.append(tdRussianTitle); // Русское название первым
                tr.append(tdOriginalTitle); // Оригинальное название вторым
                tr.append(tdYear);
                tr.append(tdActions);

                // Добавляем строку в таблицу
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
    // Очищаем сообщения об ошибках
    document.getElementById('error-message').innerText = '';
    document.getElementById('description-error').innerText = '';

    // Отображаем модальное окно
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
        title: document.getElementById('title').value.trim(), // Удаляем пробелы
        title_ru: document.getElementById('title-ru').value.trim(), // Удаляем пробелы
        year: parseInt(document.getElementById('year').value), // Преобразуем в число
        description: document.getElementById('description').value.trim() // Удаляем пробелы
    };

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList(); // Обновляем таблицу
            hideModal();
            return {};
        }
        return resp.json(); // Если есть ошибки, парсим их
    })
    .then(function(errors) {
        let errorMessage = '';
        if(errors.title_ru) {
            errorMessage += errors.title_ru + '\n';
        }
        if(errors.title) {
            errorMessage += errors.title + '\n';
        }
        if(errors.year) {
            errorMessage += errors.year + '\n';
        }
        if(errors.description) {
            errorMessage += errors.description + '\n';
            document.getElementById('description-error').innerText = errors.description;
        }
        if (errorMessage) {
            document.getElementById('error-message').innerText = errorMessage;
        }
    })
    .catch(function(error) {
        console.error('Ошибка при отправке данных:', error);
        document.getElementById('error-message').innerText = 'Произошла ошибка при отправке данных. Пожалуйста, попробуйте позже.';
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