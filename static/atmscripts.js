document.addEventListener('DOMContentLoaded', function() {
    const errorTableBody = document.querySelector('#errorTable tbody');
    const statusTableBody = document.querySelector('#statusTable tbody');
    const errorFilter = document.getElementById('errorFilter');
    const prevErrorPageButton = document.getElementById('prevErrorPage');
    const nextErrorPageButton = document.getElementById('nextErrorPage');
    const errorPageInfo = document.getElementById('errorPageInfo');
    const prevStatusPageButton = document.getElementById('prevStatusPage');
    const nextStatusPageButton = document.getElementById('nextStatusPage');
    const statusPageInfo = document.getElementById('statusPageInfo');
    const addAtmButton = document.getElementById('addAtmButton');
    const addAtmForm = document.getElementById('addAtmForm');
    const addressInput = document.getElementById('address');
    const coordsInput = document.getElementById('coords');

    let atmData = {};
    let atmStatus = {};
    let currentPageErrors = 1;
    let currentPageStatuses = 1;
    const itemsPerPage = 9;

    fetch('/get_atm_data')
        .then(response => response.json())
        .then(data => {
            atmData = data;
            renderErrors();
        });

    fetch('/get_atm_status')
        .then(response => response.json())
        .then(data => {
            atmStatus = data;
            renderStatuses();
        });

    errorFilter.addEventListener('change', () => {
        currentPageErrors = 1;
        renderErrors();
    });

    prevErrorPageButton.addEventListener('click', () => {
        if (currentPageErrors > 1) {
            currentPageErrors--;
            renderErrors();
        }
    });

    nextErrorPageButton.addEventListener('click', () => {
        const totalPages = Math.ceil(getFilteredErrors().length / itemsPerPage);
        if (currentPageErrors < totalPages) {
            currentPageErrors++;
            renderErrors();
        }
    });

    prevStatusPageButton.addEventListener('click', () => {
        if (currentPageStatuses > 1) {
            currentPageStatuses--;
            renderStatuses();
        }
    });

    nextStatusPageButton.addEventListener('click', () => {
        const totalPages = Math.ceil(Object.keys(atmStatus).length / itemsPerPage);
        if (currentPageStatuses < totalPages) {
            currentPageStatuses++;
            renderStatuses();
        }
    });

    addAtmButton.addEventListener('click', () => {
        addAtmForm.style.display = addAtmForm.style.display === 'none' ? 'block' : 'none';
    });

    addAtmForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const address = addressInput.value;
        const coords = coordsInput.value;

        // Генерация нового уникального ID для банкомата
        const newAtmId = generateNewAtmId(atmStatus);

        atmStatus[newAtmId] = {
            lvl: 0,
            askfor: "None",
            address: address,
            coords: coords
        };

        saveJson(atmStatus, '/save_atm_status');
        addAtmForm.style.display = 'none';
        clearForm();
        renderStatuses();
    });

    function renderErrors() {
        errorTableBody.innerHTML = '';
        const filterValue = errorFilter.value;
        const errors = getFilteredErrors();

        const startIndex = (currentPageErrors - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const paginatedErrors = errors.slice(startIndex, endIndex);

        paginatedErrors.forEach(error => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${error.date} - ${error.id}</td>
                <td>${error.error}</td>
            `;
            errorTableBody.appendChild(row);
        });

        updatePaginationInfo(errors.length, currentPageErrors, itemsPerPage, 'error');
    }

    function getFilteredErrors() {
        const filterValue = errorFilter.value;
        let errors = [];

        switch (filterValue) {
            case 'errors':
                errors = atmData.errors;
                break;
            case 'criticalErrors':
                errors = atmData.critical_errors;
                break;
            default:
                errors = [
                    ...atmData.critical_errors,
                    ...atmData.errors,
                    ...atmData.non_errors
                ];
        }

        return errors;
    }

    function renderStatuses() {
        statusTableBody.innerHTML = '';
        const atmIds = Object.keys(atmStatus);

        const startIndex = (currentPageStatuses - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const paginatedStatuses = atmIds.slice(startIndex, endIndex);

        paginatedStatuses.forEach(atmId => {
            const atm = atmStatus[atmId];
            const row = document.createElement('tr');
            const lvl = atm.lvl;
            const askfor = atm.askfor;
            row.className = lvl === 1 ? 'yellow' : lvl === 2 ? 'red' : '';

            row.innerHTML = `
                <td>${atmId}</td>
                <td>${askfor}</td>
                <td><button onclick="deleteAtm('${atmId}')">Удалить</button></td>
            `;
            statusTableBody.appendChild(row);
        });

        updatePaginationInfo(atmIds.length, currentPageStatuses, itemsPerPage, 'status');
    }

    function updatePaginationInfo(totalItems, currentPage, itemsPerPage, tableType) {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        const pageInfoElement = tableType === 'error' ? errorPageInfo : statusPageInfo;
        pageInfoElement.textContent = `Страница ${currentPage} из ${totalPages}`;
        
        const prevButton = tableType === 'error' ? prevErrorPageButton : prevStatusPageButton;
        const nextButton = tableType === 'error' ? nextErrorPageButton : nextStatusPageButton;

        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
    }

    window.deleteAtm = function(atmId) {
        delete atmStatus[atmId];
        saveJson(atmStatus, '/save_atm_status');
        renderStatuses();
    };

    function saveJson(data, url) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .catch(error => console.error('Ошибка сохранения:', error));
    }

    function generateNewAtmId(atmStatus) {
        const atmIds = Object.keys(atmStatus);
        let newId = 1;
        while (atmIds.includes(`Банкомат${newId}`)) {
            newId++;
        }
        return `Банкомат${newId}`;
    }

    function clearForm() {
        addressInput.value = '';
        coordsInput.value = '';
    }
});