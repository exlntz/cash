document.addEventListener('DOMContentLoaded', () => {
    const atmErrorsTableBody = document.querySelector('#atm_errors_table tbody');
    const atmStatusTableBody = document.querySelector('#atm_status_table tbody');
    const atmSelector = document.getElementById('atm_selector');
    const errorFilter = document.getElementById('error_filter');
    const statusFilter = document.getElementById('status_filter');
    const sortByIDButton = document.getElementById('sort_by_id');
    const addAtmButton = document.getElementById('add_atm_button');
    const addAtmForm = document.getElementById('add_atm_form');
    const atmDetails = document.getElementById('atm_details');
    const currentStatus = document.getElementById('current_status');
    const workPercentage = document.getElementById('work_percentage');
    const weeklyErrorsChartCanvas = document.getElementById('weekly_errors_chart').getContext('2d');
    const monthlyErrorsChartCanvas = document.getElementById('monthly_errors_chart').getContext('2d');

    let atmData = {};
    let atmStatus = {};
    let atmWorkingTimePercent = {};
    let atmErrorsData = {};

    // Постраничный вывод
    let currentPageErrors = 1;
    let currentPageStatus = 1;
    const itemsPerPage = 9;

    // Функции для загрузки данных
    async function loadAtmData() {
        const response = await fetch('/get_atm_data');
        atmData = await response.json();
        renderAtmErrorsTable();
    }

    async function loadAtmStatus() {
        const response = await fetch('/get_atm_status');
        atmStatus = await response.json();
        renderAtmStatusTable();
        populateAtmSelector();
    }

    async function loadAtmWorkingTimePercent() {
        const response = await fetch('/get_atm_working_time_percent');
        atmWorkingTimePercent = await response.json();
    }

    async function loadAtmErrorsData() {
        const response = await fetch('/get_atm_errors_data');
        atmErrorsData = await response.json();
    }

    // Функции для рендера таблиц
    function renderAtmErrorsTable(page = 1) {
        atmErrorsTableBody.innerHTML = '';
        const filteredErrors = filterErrorsData();
        const paginatedErrors = paginate(filteredErrors, page, itemsPerPage);
        paginatedErrors.forEach(error => {
            const row = document.createElement('tr');
            row.classList.add(error.type);
            row.innerHTML = `
                <td>${error.id}</td>
                <td>${error.date}</td>
                <td>${error.error}</td>
            `;
            atmErrorsTableBody.appendChild(row);
        });
        renderPagination(filteredErrors.length, page, 'errors');
    }

    function renderAtmStatusTable(page = 1) {
        atmStatusTableBody.innerHTML = '';
        const filteredStatuses = filterStatusData();
        const paginatedStatuses = paginate(filteredStatuses, page, itemsPerPage);
        paginatedStatuses.forEach(status => {
            const row = document.createElement('tr');
            row.setAttribute('data-id', status.id);
            row.setAttribute('data-status', status.status);
            row.innerHTML = `
                <td>${status.id}</td>
                <td>${getStatusText(status.status)}</td>
                <td><button class="delete_atm" data-id="${status.id}">Удалить</button></td>
            `;
            atmStatusTableBody.appendChild(row);
        });
        renderPagination(filteredStatuses.length, page, 'status');
    }

    function populateAtmSelector() {
        atmSelector.innerHTML = '<option value="">Выберите банкомат</option>';
        for (const atmId in atmStatus) {
            const option = document.createElement('option');
            option.value = atmId;
            option.textContent = atmId;
            atmSelector.appendChild(option);
        }
    }

    // Функции для фильтрации и сортировки
    function filterErrorsData() {
        const filterType = errorFilter.value;
        const allErrors = [];
        for (const errorType of ['critical_errors', 'errors', 'non_errors']) {
            atmData[errorType].forEach(error => {
                error.type = errorType;
                allErrors.push(error);
            });
        }
        return filterType === 'all' ? allErrors : allErrors.filter(error => error.type === filterType);
    }

    function filterStatusData() {
        const statusType = statusFilter.value;
        const statuses = [];
        for (const atmId in atmStatus) {
            const status = atmStatus[atmId].askfor;
            statuses.push({ id: atmId, status });
        }
        return statusType === 'all' ? statuses : statuses.filter(status => status.status === statusType);
    }

    function sortByID() {
        const rows = Array.from(atmStatusTableBody.querySelectorAll('tr'));
        rows.sort((a, b) => {
            const idA = parseInt(a.getAttribute('data-id').replace('Банкомат', ''), 10);
            const idB = parseInt(b.getAttribute('data-id').replace('Банкомат', ''), 10);
            return idA - idB;
        });
        rows.forEach(row => atmStatusTableBody.appendChild(row));
    }

    // Функции для постраничного вывода
    function paginate(array, page, itemsPerPage) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return array.slice(start, end);
    }

    function renderPagination(totalItems, currentPage, tableType) {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        const paginationContainer = document.getElementById(`${tableType}_pagination`);
        if (!paginationContainer) {
            const container = document.createElement('div');
            container.id = `${tableType}_pagination`;
            container.className = 'pagination';
            document.querySelector(`#${tableType}_table`).insertAdjacentElement('afterend', container);
        }
        paginationContainer.innerHTML = '';

        if (totalPages > 1) {
            const prevButton = document.createElement('button');
            prevButton.textContent = 'Предыдущая';
            prevButton.disabled = currentPage === 1;
            prevButton.addEventListener('click', () => {
                if (currentPage > 1) {
                    if (tableType === 'errors') {
                        renderAtmErrorsTable(currentPage - 1);
                        currentPageErrors = currentPage - 1;
                    } else if (tableType === 'status') {
                        renderAtmStatusTable(currentPage - 1);
                        currentPageStatus = currentPage - 1;
                    }
                }
            });
            paginationContainer.appendChild(prevButton);

            const startPage = Math.max(1, currentPage - 2);
            const endPage = Math.min(totalPages, currentPage + 2);

            for (let i = startPage; i <= endPage; i++) {
                const pageButton = document.createElement('button');
                pageButton.textContent = i;
                pageButton.disabled = currentPage === i;
                pageButton.addEventListener('click', () => {
                    if (tableType === 'errors') {
                        renderAtmErrorsTable(i);
                        currentPageErrors = i;
                    } else if (tableType === 'status') {
                        renderAtmStatusTable(i);
                        currentPageStatus = i;
                    }
                });
                paginationContainer.appendChild(pageButton);
            }

            const nextButton = document.createElement('button');
            nextButton.textContent = 'Следующая';
            nextButton.disabled = currentPage === totalPages;
            nextButton.addEventListener('click', () => {
                if (currentPage < totalPages) {
                    if (tableType === 'errors') {
                        renderAtmErrorsTable(currentPage + 1);
                        currentPageErrors = currentPage + 1;
                    } else if (tableType === 'status') {
                        renderAtmStatusTable(currentPage + 1);
                        currentPageStatus = currentPage + 1;
                    }
                }
            });
            paginationContainer.appendChild(nextButton);
        }
    }

    // Обработчики событий
    errorFilter.addEventListener('change', () => {
        currentPageErrors = 1;
        renderAtmErrorsTable();
    });

    statusFilter.addEventListener('change', () => {
        currentPageStatus = 1;
        renderAtmStatusTable();
    });

    sortByIDButton.addEventListener('click', sortByID);

    addAtmButton.addEventListener('click', () => addAtmForm.style.display = 'block');

    document.getElementById('add_atm_form_inner').addEventListener('submit', async (e) => {
        e.preventDefault();
        const address = document.getElementById('address').value;
        const coords = document.getElementById('coords').value;

        const response = await fetch('/add_atm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `address=${encodeURIComponent(address)}&coords=${encodeURIComponent(coords)}`,
        });

        const result = await response.json();
        if (result.success) {
            addAtmForm.style.display = 'none';
            document.getElementById('address').value = '';
            document.getElementById('coords').value = '';
            loadAtmStatus();  // Обновляем список банкоматов
        } else {
            alert(result.message);
        }
    });

    atmStatusTableBody.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete_atm')) {
            const atmId = e.target.getAttribute('data-id');
            const response = await fetch(`/delete_atm/${atmId}`, { method: 'POST' });
            const result = await response.json();
            if (result.success) {
                e.target.closest('tr').remove();
                atmSelector.querySelector(`option[value="${atmId}"]`).remove();
            }
        }
    });

    atmSelector.addEventListener('change', () => {
        const atmId = atmSelector.value;
        if (atmId) {
            const status = atmStatus[atmId].askfor;
            const percentage = atmWorkingTimePercent[atmId];
            currentStatus.textContent = getStatusText(status);
            workPercentage.textContent = `Процент работы за месяц: ${percentage.Percent}%`;

            // Процент работы за неделю
            const weekTime = atmWorkingTimePercent[atmId].timeON / 7; // Предполагаем, что месяц 30 дней
            const weekPercentage = (weekTime / atmWorkingTimePercent[atmId].timeON) * 100;
            document.getElementById('work_percentage').textContent += `, за неделю: ${weekPercentage.toFixed(2)}%`;

            const weekErrors = [];
            const monthErrors = [];

            for (const month in atmErrorsData) {
                for (const week in atmErrorsData[month]) {
                    const errors = atmErrorsData[month][week][atmId] || [];
                    if (month === Object.keys(atmErrorsData)[Object.keys(atmErrorsData).length - 1]) {
                        weekErrors.push(errors.length);
                    }
                    monthErrors.push(errors.length);
                }
            }

            new Chart(weeklyErrorsChartCanvas, {
                type: 'bar',
                data: {
                    labels: Array.from({ length: weekErrors.length }, (_, i) => `Неделя ${i + 1}`),
                    datasets: [{
                        label: 'Количество ошибок за неделю',
                        data: weekErrors,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            new Chart(monthlyErrorsChartCanvas, {
                type: 'line',
                data: {
                    labels: Array.from({ length: monthErrors.length }, (_, i) => `Неделя ${i + 1}`),
                    datasets: [{
                        label: 'Количество ошибок за месяц',
                        data: monthErrors,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            atmDetails.style.display = 'block';
        } else {
            atmDetails.style.display = 'none';
        }
    });

    // Вспомогательные функции
    function getStatusText(status) {
        switch (status) {
            case 'incass':
                return 'Требуется инкассация';
            case 'service':
                return 'Требуется обслуживание';
            default:
                return 'Без ошибок';
        }
    }

    // Инициализация данных
    Promise.all([
        loadAtmData(),
        loadAtmStatus(),
        loadAtmWorkingTimePercent(),
        loadAtmErrorsData()
    ]).then(() => {
        renderAtmErrorsTable();
        renderAtmStatusTable();
    });
});