import json
from geopy.distance import geodesic

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def sort_atms(atms):
    return sorted(atms, key=lambda x: x['lvl'], reverse=True)

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).km

def nearest_atm(current, remaining_atms):
    nearest = None
    min_distance = float('inf')
    
    for atm in remaining_atms:
        distance = calculate_distance(current['coords'], atm['coords'])
        if distance < min_distance:
            min_distance = distance
            nearest = atm
    return nearest
def create_greedy_route(atms, start_point):
    route = [start_point]
    remaining_atms = atms[:]
    while remaining_atms:
        nearest = nearest_atm(route[-1], remaining_atms)
        route.append(nearest)
        remaining_atms.remove(nearest)
    route.append(start_point)
    return route
def distribute_atms(atms, num_machines):
    chunk_size = len(atms) // num_machines
    routes = []
    for i in range(num_machines):
        route = atms[i*chunk_size:(i+1)*chunk_size]
        routes.append(route)
    return routes

def main():
    atms_data = load_data('static/jsons/AtmStatus.json')
    service_atms = []
    incass_atms = []
    start_point = {'atm': 'start', 'coords': (55.756315, 37.614716), 'lvl': 0}
    for atm, details in atms_data.items():
        if details['askfor'] == 'service' and details['lvl'] > 0:
            coords = tuple(map(float, details['coords'].split(', ')))
            service_atms.append({'atm': atm, 'coords': coords, 'lvl': details['lvl']})
        elif details['askfor'] == 'incass' and details['lvl'] > 0:
            coords = tuple(map(float, details['coords'].split(', ')))
            incass_atms.append({'atm': atm, 'coords': coords, 'lvl': details['lvl']})
    service_atms = sort_atms(service_atms)
    incass_atms = sort_atms(incass_atms)
    cars = load_data('static/jsons/cars.json')
    mech = load_data('static/jsons/mechanics.json')
    num_service_machines = len(mech)
    num_incass_machines = len(cars)
    service_routes = distribute_atms(service_atms, num_service_machines)
    incass_routes = distribute_atms(incass_atms, num_incass_machines)
    optimized_service_routes = [create_greedy_route(route, start_point) for route in service_routes]
    optimized_incass_routes = [create_greedy_route(route, start_point) for route in incass_routes]
    routes = {
        'service_routes': optimized_service_routes,
        'incass_routes': optimized_incass_routes
    }
    with open('static/jsons/routes.json', 'w', encoding='utf-8') as f:
        json.dump(routes, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
