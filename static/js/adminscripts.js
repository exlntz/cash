document.addEventListener('DOMContentLoaded', function() {
    const mechanicsTableBody = document.querySelector('#mechanicsTable tbody');
    const carsTableBody = document.querySelector('#carsTable tbody');
    const prevMechanicsPageButton = document.getElementById('prevMechanicsPage');
    const nextMechanicsPageButton = document.getElementById('nextMechanicsPage');
    const mechanicsPageInfo = document.getElementById('mechanicsPageInfo');
    const prevCarsPageButton = document.getElementById('prevCarsPage');
    const nextCarsPageButton = document.getElementById('nextCarsPage');
    const carsPageInfo = document.getElementById('carsPageInfo');
    const addMechanicButton = document.getElementById('addMechanicButton');
    const addMechanicForm = document.getElementById('addMechanicForm');
    const addCarButton = document.getElementById('addCarButton');
    const addCarForm = document.getElementById('addCarForm');

    let mechanics = {};
    let cars = {};
    let currentPageMechanics = 1;
    let currentPageCars = 1;
    const itemsPerPage = 9;

    fetch('/get_mechanics')
        .then(response => response.json())
        .then(data => {
            mechanics = data;
            renderMechanics();
        })
        .catch(error => console.error('Ошибка загрузки механиков:', error));

    fetch('/get_cars')
        .then(response => response.json())
        .then(data => {
            cars = data;
            renderCars();
        })
        .catch(error => console.error('Ошибка загрузки машин:', error));

    prevMechanicsPageButton.addEventListener('click', () => {
        if (currentPageMechanics > 1) {
            currentPageMechanics--;
            renderMechanics();
        }
    });

    nextMechanicsPageButton.addEventListener('click', () => {
        const totalPages = Math.ceil(Object.keys(mechanics).length / itemsPerPage);
        if (currentPageMechanics < totalPages) {
            currentPageMechanics++;
            renderMechanics();
        }
    });

    prevCarsPageButton.addEventListener('click', () => {
        if (currentPageCars > 1) {
            currentPageCars--;
            renderCars();
        }
    });

    nextCarsPageButton.addEventListener('click', () => {
        const totalPages = Math.ceil(Object.keys(cars).length / itemsPerPage);
        if (currentPageCars < totalPages) {
            currentPageCars++;
            renderCars();
        }
    });

    addMechanicButton.addEventListener('click', () => {
        addMechanicForm.style.display = 'block';
    });

    document.getElementById('cancelMechanicForm').addEventListener('click', () => {
        addMechanicForm.style.display = 'none';
    });

    addMechanicForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const name = document.getElementById('mechanicName').value;
        const age = parseInt(document.getElementById('mechanicAge').value, 10);

        const newMechanicId = generateNewMechanicId(mechanics);
        mechanics[newMechanicId] = {
            Name: name,
            Age: age
        };

        saveJson(mechanics, '/save_mechanics')
            .then(() => {
                addMechanicForm.style.display = 'none';
                clearMechanicForm();
                renderMechanics();
                showNotification('Механик добавлен');
            })
            .catch(error => console.error('Ошибка сохранения механика:', error));
    });

    addCarButton.addEventListener('click', () => {
        addCarForm.style.display = 'block';
    });

    document.getElementById('cancelCarForm').addEventListener('click', () => {
        addCarForm.style.display = 'none';
    });

    addCarForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const name = document.getElementById('carName').value;
        const plate = document.getElementById('carPlate').value;

        const newCarId = generateNewCarId(cars);
        cars[newCarId] = {
            Name: name,
            plate: plate
        };

        saveJson(cars, '/save_cars')
            .then(() => {
                addCarForm.style.display = 'none';
                clearCarForm();
                renderCars();
                showNotification('Машина инкассации добавлена');
            })
            .catch(error => console.error('Ошибка сохранения машины:', error));
    });

    function renderMechanics() {
        mechanicsTableBody.innerHTML = '';
        const mechanicIds = Object.keys(mechanics);

        const startIndex = (currentPageMechanics - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const paginatedMechanics = mechanicIds.slice(startIndex, endIndex);

        paginatedMechanics.forEach(mechanicId => {
            const mechanic = mechanics[mechanicId];
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${mechanicId}</td>
                <td>${mechanic.Name}</td>
                <td>${mechanic.Age}</td>
                <td><button onclick="deleteMechanic('${mechanicId}')">Удалить</button></td>
            `;
            mechanicsTableBody.appendChild(row);
        });

        updatePaginationInfo(mechanicIds.length, currentPageMechanics, itemsPerPage, 'mechanics');
    }

    function renderCars() {
        carsTableBody.innerHTML = '';
        const carIds = Object.keys(cars);

        const startIndex = (currentPageCars - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const paginatedCars = carIds.slice(startIndex, endIndex);

        paginatedCars.forEach(carId => {
            const car = cars[carId];
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${carId}</td>
                <td>${car.Name}</td>
                <td>${car.plate}</td>
                <td><button onclick="deleteCar('${carId}')">Удалить</button></td>
            `;
            carsTableBody.appendChild(row);
        });

        updatePaginationInfo(carIds.length, currentPageCars, itemsPerPage, 'cars');
    }

    function updatePaginationInfo(totalItems, currentPage, itemsPerPage, tableType) {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        const pageInfoElement = tableType === 'mechanics' ? mechanicsPageInfo : carsPageInfo;
        pageInfoElement.textContent = `Страница ${currentPage} из ${totalPages}`;
        
        const prevButton = tableType === 'mechanics' ? prevMechanicsPageButton : prevCarsPageButton;
        const nextButton = tableType === 'mechanics' ? nextMechanicsPageButton : nextCarsPageButton;

        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
    }

    window.deleteMechanic = function(mechanicId) {
        delete mechanics[mechanicId];
        saveJson(mechanics, '/save_mechanics')
            .then(() => renderMechanics())
            .catch(error => console.error('Ошибка удаления механика:', error));
    };

    window.deleteCar = function(carId) {
        delete cars[carId];
        saveJson(cars, '/save_cars')
            .then(() => renderCars())
            .catch(error => console.error('Ошибка удаления машины:', error));
    };

    function saveJson(data, url) {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сохранения данных');
            }
            return response.json();
        });
    }

    function generateNewMechanicId(mechanics) {
        const mechanicIds = Object.keys(mechanics);
        let newId = 1;
        while (mechanicIds.includes(`Механик${newId}`)) {
            newId++;
        }
        return `Механик${newId}`;
    }

    function generateNewCarId(cars) {
        const carIds = Object.keys(cars);
        let newId = 1;
        while (carIds.includes(`Машина${newId}`)) {
            newId++;
        }
        return `Машина${newId}`;
    }

    function clearMechanicForm() {
        document.getElementById('mechanicName').value = '';
        document.getElementById('mechanicAge').value = '';
    }

    function clearCarForm() {
        document.getElementById('carName').value = '';
        document.getElementById('carPlate').value = '';
    }

    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('hide');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 3000);
    }
});