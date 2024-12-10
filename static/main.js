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
                    editFilm(films[i].id); // Передаем id фильма
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = function () {
                    deleteFilm(films[i].id, films[i].title_ru); // Передаем id и название фильма
                };

                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавляем ячейки в строку
                tr.append(tdRussianTitle); // Русское название
                tr.append(tdOriginalTitle); // Оригинальное название
                tr.append(tdYear); // Год
                tr.append(tdActions); // Действия

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
    // Очищаем поля формы
    document.getElementById('film-id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';

    showModal();
}

function editFilm(id) {
    console.log(`Fetching film with id: ${id}`);  // Отладочное сообщение
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function(response) {
        if (!response.ok) {
            throw new Error(`Failed to fetch film with id ${id}`);
        }
        return response.json();
    })
    .then(function(film) {
        console.log(`Film data received:`, film);  // Отладочное сообщение
        // Заполняем поля формы
        document.getElementById('film-id').value = film.id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    })
    .catch(function(error) {
        console.error('Ошибка при получении данных фильма:', error);
        alert('Не удалось получить данные фильма. Пожалуйста, попробуйте позже.');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();

    document.getElementById('add-film-button').addEventListener('click', addFilm);
});

function sendFilm() {
    const film = {
        title: document.getElementById('title').value.trim(), // Удаляем пробелы
        title_ru: document.getElementById('title-ru').value.trim(), // Удаляем пробелы
        year: parseInt(document.getElementById('year').value), // Преобразуем в число
        description: document.getElementById('description').value.trim() // Удаляем пробелы
    };

    // Проверяем, редактируем ли мы существующий фильм
    const id = document.getElementById('film-id').value; // Получаем id из скрытого поля
    const url = id ? `/lab7/rest-api/films/${id}` : '/lab7/rest-api/films/';
    const method = id ? 'PUT' : 'POST';

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
        if(errors.error) { // Ошибка, возвращаемая сервером
            errorMessage += errors.error + '\n';
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