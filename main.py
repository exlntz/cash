from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import csv
import pandas as pd

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_def():
    return render_template('home/home.html')

@app.route('/atm')  # Automated teller machine
def atm_def():
    return render_template('atms/atm.html')

@app.route('/maps')
def maps_def():
    return render_template('maps/maps.html')

@app.route('/admin')
def admin_def():
    # Загрузка данных из CSV файлов
    mechanics_csv = pd.read_csv('csvfiles/mechanics.csv').to_dict(orient='records')
    cars_csv = pd.read_csv('csvfiles/cars.csv').to_dict(orient='records')
    return render_template('admin/admin.html', mechanics=mechanics_csv, cars=cars_csv)

@app.route('/get_atm_data')
def get_atm_data():
    with open('jsons/atm_data.json', 'r', encoding='utf-8') as f:
        atm_data = json.load(f)
    return jsonify(atm_data)

@app.route('/get_atm_status')
def get_atm_status():
    with open('jsons/atmstatus.json', 'r', encoding='utf-8') as f:
        atm_status = json.load(f)
    return jsonify(atm_status)

@app.route('/save_atm_status', methods=['POST'])
def save_atm_status():
    data = request.get_json()
    with open('jsons/atmstatus.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify({'success': True})

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)



#@app.route('/save_mechanic', methods=['POST'])
#def save_mechanic():
   # data = request.get_json()
   # name = data['name']
   # age = data['age']

    # Сохранение данных в mechanics.csv
  # with open('csvfiles/mechanics.csv', 'a', encoding='utf-8', newline='') as fm:
   #     csv.writer(fm).writerow([name, age])
   # return jsonify({'success': True})

#@app.route('/save_car', methods=['POST'])
#def save_car_def():
   # data = request.get_json()
   # name = data['name']
   # plate = data['plate']

    # Сохранение данных в cars.csv
   # with open('csvfiles/cars.csv', 'a', encoding='utf-8', newline='') as fc:
  #      csv.writer(fc).writerow([name, plate])
  #  return jsonify({'success': True})


MECHANICS_FILE = 'csvfiles/mechanics.csv'
CARS_FILE = 'csvfiles/cars.csv'

def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@app.route('/save_mechanic', methods=['POST'])
def save_mechanic():
    data = request.json
    mechanics = read_csv(MECHANICS_FILE)
    mechanics.append(data)
    write_csv(MECHANICS_FILE, mechanics, ['name', 'age'])
    return jsonify({'success': True})

@app.route('/delete_mechanic', methods=['POST'])
def delete_mechanic():
    data = request.json
    mechanics = read_csv(MECHANICS_FILE)
    mechanics = [mech for mech in mechanics if mech['name'] != data['name'] or mech['age'] != str(data['age'])]
    write_csv(MECHANICS_FILE, mechanics, ['name', 'age'])
    return jsonify({'success': True})

@app.route('/save_car', methods=['POST'])
def save_car():
    data = request.json
    cars = read_csv(CARS_FILE)
    cars.append(data)
    write_csv(CARS_FILE, cars, ['name', 'plate'])
    return jsonify({'success': True})

@app.route('/delete_car', methods=['POST'])
def delete_car():
    data = request.json
    cars = read_csv(CARS_FILE)
    cars = [car for car in cars if car['name'] != data['name'] or car['plate'] != data['plate']]
    write_csv(CARS_FILE, cars, ['name', 'plate'])
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)