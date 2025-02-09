let map;
let routesData = {};  // Object to store the routes data after loading from routes.json
let routeType = "service_routes";  // Default route type
const routeSelect = document.getElementById('route');

// Initialize the map
function initMap() {
    map = new ymaps.Map("map", {
        center: [55.7522, 37.6156], // Центр карты (Москва)
        zoom: 10
    });
    fetchRoutes(); // Load routes data from routes.json
}

// Fetch routes data from routes.json
function fetchRoutes() {
    fetch('static/jsons/routes.json')
        .then(response => response.json())
        .then(data => {
            routesData = data;
            updateRoutes();  // Populate the route options after fetching data
        })
        .catch(error => {
            console.error("Error loading routes:", error);
        });
}

// Update the route options based on the selected route type
function updateRoutes() {
    if (!routesData[routeType]) {
        return; // If no routes data is available for the selected type, do nothing
    }

    routeSelect.innerHTML = '';  // Clear existing options

    const selectedRoutes = routesData[routeType];
    selectedRoutes.forEach((route, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `Маршрут ${index + 1}`;
        routeSelect.appendChild(option);
    });
}

// Create the route from Depot to Depot, passing through all ATMs
function createRoute() {
    const selectedRoute = routesData[routeType][routeSelect.value];
    if (!selectedRoute) return;

    const points = selectedRoute.map(point => point.coords);
    const startPoint = points[0];
    const endPoint = points[points.length - 1];

    const multiRoute = new ymaps.multiRouter.MultiRoute({
        referencePoints: points,
        params: { routingMode: 'auto' }
    }, {
        boundsAutoApply: true
    });

    map.geoObjects.removeAll();
    map.geoObjects.add(multiRoute);

    points.forEach((point, index) => {
        const pointData = selectedRoute[index]; // Get point data
        let markerOptions = { balloonContent: 'ATM' };

        // Преобразование lvl в число для проверки
        const lvl = Number(pointData.lvl); // Преобразуем в число для сравнения

        // Если lvl == 2, то устанавливаем красную метку
        if (lvl === 2) {
            markerOptions = {
                iconLayout: 'default#image',
                iconImageHref: '/static/img/warn.png', // Путь к красной метке
                iconImageSize: [30, 30],
                iconImageOffset: [-15, -15]
            };
        } else {
        }

        const marker = new ymaps.Placemark(point, markerOptions);
        map.geoObjects.add(marker);
    });

    map.setCenter(startPoint, 12);
}

// Event listener for route type change
document.getElementById('routeType').addEventListener('change', function () {
    routeType = this.value;
    updateRoutes();  // Update route options when route type changes
});

// Initialize the map and setup event listeners
ymaps.ready(initMap);
