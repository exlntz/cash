const outputElement = document.getElementById('output');
const filterButtons = document.querySelectorAll('.filter-btn');
// Загрузка и отображение данных
async function loadData() {
    const response = await fetch('../../jsons/atm_data.json');
    const data = await response.json();
    return data;
}
function formatDate(dateString) {
    const date = new Date(dateString);
    return `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
}
function displayData(data) {
    outputElement.innerHTML = ''; // Очистка предыдущего вывода
    data.forEach(item => {
        const errorString = `${formatDate(item.date)} - Банкомат(${item.id}) - ${item.error}`;
        const div = document.createElement('div');
        div.textContent = errorString;
        outputElement.appendChild(div);
    });
}
// Фильтрация и сортировка данных
async function filterData(filter) {
    const data = await loadData();

    let filteredData = [];
    if (filter === 'all') {
        filteredData = [...data.criticalerrors, ...data.errors, ...data.nonerrors];
    } else if (filter === 'errors') {
        filteredData = [...data.errors];
    } else if (filter === 'critical') {
        filteredData = [...data.criticalerrors];
    }
    // Сортировка
    filteredData.sort((a, b) => {
        return a.id - b.id || new Date(a.date) - new Date(b.date);
    });
    displayData(filteredData);
}
// Добавление обработчиков событий для кнопок фильтрации
filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        const filter = button.getAttribute('data-filter');
        filterData(filter);
    });
});
// Инициализация
filterData('all');