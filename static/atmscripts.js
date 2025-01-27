document.addEventListener('DOMContentLoaded', function() {
    const errorTableBody = document.querySelector('#errorTable tbody');
    const statusTableBody = document.querySelector('#statusTable tbody');
    const errorFilter = document.getElementById('errorFilter');
    const addAtmButton = document.getElementById('addAtmButton');
    const addAtmForm = document.getElementById('addAtmForm');

    let atmData = {};
    let atmStatus = {};

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

    errorFilter.addEventListener('change', renderErrors);

    addAtmButton.addEventListener('click', () => {
        addAtmForm.style.display = addAtmForm.style.display === 'none' ? 'block' : 'none';
    });

    addAtmForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const address = document.getElementById('address').value;
        const coords = document.getElementById('coords').value;

        for (const atm in atmStatus) {
            if (address) atmStatus[atm].address = address;
            if (coords) atmStatus[atm].coords = coords;
        }

        saveJson(atmStatus, '/save_atm_status');
        addAtmForm.style.display = 'none';
        renderStatuses();
    });

    function renderErrors() {
        errorTableBody.innerHTML = '';
        const filterValue = errorFilter.value;
        let errors = [];

        switch (filterValue) {
            case 'errors':
                errors = Object.values(atmData.errors);
                break;
            case 'criticalErrors':
                errors = Object.values(atmData.Criticalerrors);
                break;
            default:
                errors = [
                    ...Object.values(atmData.errors),
                    ...Object.values(atmData.Criticalerrors),
                    ...Object.values(atmData.nonerrors)
                ];
        }

        errors.forEach(error => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${error.date} - ${error.id}</td>
                <td>${error.error}</td>
            `;
            errorTableBody.appendChild(row);
        });
    }

    function renderStatuses() {
        statusTableBody.innerHTML = '';
        for (const atm in atmStatus) {
            const row = document.createElement('tr');
            const lvl = atmStatus[atm].lvl;
            const askfor = atmStatus[atm].askfor;
            row.className = lvl === 1 ? 'yellow' : lvl === 2 ? 'red' : '';

            row.innerHTML = `
                <td>${atm}</td>
                <td>${askfor}</td>
                <td><button onclick="deleteAtm('${atm}')">Удалить</button></td>
            `;
            statusTableBody.appendChild(row);
        }
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
});