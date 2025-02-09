import json
from math import radians, sin, cos, sqrt, atan2

# Функция для расчета расстояния между двумя точками по их координатам (Haversine formula)
def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371.0  # Радиус Земли в километрах

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Функция для создания маршрутов
def create_routes(n_service_cars, m_incass_cars):
    # Начальная точка (Кремль, Москва)
    depot_coords = (55.7522, 37.6156)

    # Чтение данных из файла
    with open("static/jsons/AtmStatus.json", "r", encoding="utf-8") as file:
        atm_data = json.load(file)

    # Фильтрация банкоматов по lvl и askfor
    service_atms = []
    incass_atms = []

    for atm_name, atm_info in atm_data.items():
        if atm_info["lvl"] == 0 or atm_info["askfor"] == "None":
            continue
        coords = tuple(map(float, atm_info["coords"].split(", ")))
        atm_info["name"] = atm_name
        atm_info["coords"] = coords
        if atm_info["askfor"] == "service":
            service_atms.append(atm_info)
        elif atm_info["askfor"] == "incass":
            incass_atms.append(atm_info)

    # Сортировка банкоматов по приоритету (lvl=2 -> lvl=1)
    service_atms.sort(key=lambda x: x["lvl"], reverse=True)
    incass_atms.sort(key=lambda x: x["lvl"], reverse=True)

    # Функция для создания маршрутов
    def create_optimal_routes(atms, num_cars):
        routes = [[] for _ in range(num_cars)]
        distances = [0] * num_cars

        for atm in atms:
            # Находим машину с минимальным текущим расстоянием
            min_index = distances.index(min(distances))
            if not routes[min_index]:
                # Добавляем депо в начало маршрута
                routes[min_index].append({"name": "Depot", "coords": depot_coords})
            # Добавляем банкомат в маршрут
            routes[min_index].append(atm)
            # Обновляем расстояние
            last_coords = routes[min_index][-2]["coords"]
            distances[min_index] += calculate_distance(last_coords, atm["coords"])

        # Добавляем возврат в депо
        for route in routes:
            if route:
                route.append({"name": "Depot", "coords": depot_coords})

        return routes

    # Создание маршрутов
    service_routes = create_optimal_routes(service_atms, n_service_cars)
    incass_routes = create_optimal_routes(incass_atms, m_incass_cars)

    # Сохранение маршрутов в файл routes.json
    result = {
        "service_routes": service_routes,
        "incass_routes": incass_routes
    }

    with open("static/jsons/routes.json", "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print("Маршруты успешно созданы и сохранены в файл routes.json")

# Пример использования
create_routes(n_service_cars=3, m_incass_cars=4)