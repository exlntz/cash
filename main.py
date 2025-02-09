from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import uuid
import os

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_def():
    return render_template('home.html')

@app.route('/about')
def about_def():
    return render_template('about.html')

@app.route('/atm')  # Automated teller machine
def atm_def():
    return render_template('atm.html')

@app.route('/maps')
def maps_def():
    return render_template('maps.html')

@app.route('/admin')
def admin_def():
    return render_template('admin.html')

@app.route('/get_mechanics')
def get_mechanics():
    with open('jsons/mechanics.json', 'r', encoding='utf-8') as f:
        mechanics = json.load(f)
    return jsonify(mechanics)

@app.route('/save_mechanics', methods=['POST'])
def save_mechanics():
    data = request.get_json()
    with open('jsons/mechanics.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify({'success': True})

@app.route('/get_cars')
def get_cars():
    with open('jsons/cars.json', 'r', encoding='utf-8') as f:
        cars = json.load(f)
    return jsonify(cars)

@app.route('/save_cars', methods=['POST'])
def save_cars():
    data = request.get_json()
    with open('jsons/cars.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify({'success': True})

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Новые маршруты для управления банкоматами

@app.route('/get_atm_data')
def get_atm_data():
    with open('jsons/atm_data.json', 'r', encoding='utf-8') as f:
        atm_data = json.load(f)
    return jsonify(atm_data)

@app.route('/get_atm_status')
def get_atm_status():
    with open('jsons/AtmStatus.json', 'r', encoding='utf-8') as f:
        atm_status = json.load(f)
    return jsonify(atm_status)

@app.route('/get_atm_working_time_percent')
def get_atm_working_time_percent():
    with open('jsons/AtmWorkingTimePercent.json', 'r', encoding='utf-8') as f:
        atm_working_time_percent = json.load(f)
    return jsonify(atm_working_time_percent)

@app.route('/get_atm_errors_data')
def get_atm_errors_data():
    with open('jsons/atm_errors_data.json', 'r', encoding='utf-8') as f:
        atm_errors_data = json.load(f)
    return jsonify(atm_errors_data)

@app.route('/add_atm', methods=['POST'])
def add_atm():
    address = request.form.get('address')
    coords = request.form.get('coords')
    if not address and not coords:
        return jsonify({'success': False, 'message': 'Минимум одно поле должно быть заполнено'}), 400
    
    atm_id = f'Банкомат{uuid.uuid4().hex[:4]}'
    atm_status = load_json('AtmStatus.json')
    atm_status[atm_id] = {'lvl': 0, 'askfor': 'None', 'address': address, 'coords': coords}
    save_json(atm_status, 'AtmStatus.json')
    
    return jsonify({'success': True, 'id': atm_id}), 200

@app.route('/delete_atm/<atm_id>', methods=['POST'])
def delete_atm(atm_id):
    atm_data = load_json('atm_data.json')
    atm_status = load_json('AtmStatus.json')
    atm_working_time_percent = load_json('AtmWorkingTimePercent.json')
    atm_errors_data = load_json('atm_errors_data.json')
    
    # Удаление из atm_data.json
    for key in ['critical_errors', 'errors', 'non_errors']:
        atm_data[key] = [item for item in atm_data[key] if item['id'] != atm_id]
    
    # Удаление из AtmStatus.json
    atm_status.pop(atm_id, None)
    
    # Удаление из AtmWorkingTimePercent.json
    atm_working_time_percent.pop(atm_id, None)
    
    # Удаление из atm_errors_data.json
    for month in atm_errors_data.values():
        for week in month.values():
            week.pop(atm_id, None)
    
    save_json(atm_data, 'atm_data.json')
    save_json(atm_status, 'AtmStatus.json')
    save_json(atm_working_time_percent, 'AtmWorkingTimePercent.json')
    save_json(atm_errors_data, 'atm_errors_data.json')
    
    return jsonify({'success': True}), 200

def load_json(filename):
    with open(os.path.join('jsons', filename), 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, filename):
    with open(os.path.join('jsons', filename), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    app.run(debug=True)