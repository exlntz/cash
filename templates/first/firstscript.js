document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('../../jsons/users.json')
        .then(response => response.json())
        .then(users => {
            const user = users.find(user => user.username === username && user.password === password);
            if (user) {
                window.location.href = 'home.html';
            } else {
                document.getElementById('errorMessage').innerText = "Неверный логин или пароль";
                // Обнуляем значения ячеек ввода
                document.getElementById('username').value = '';
                document.getElementById('password').value = '';
            }
        })
        .catch(error => console.error('Ошибка:', error));
});