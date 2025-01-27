from flask import Flask, render_template, request, jsonify
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

@app.route('/save_mechanic', methods=['POST'])
def save_mechanic():
    data = request.get_json()
    name = data['name']
    age = data['age']
    
    # Сохранение данных в mechanics.csv
    with open('csvfiles/mechanics.csv', 'a', encoding='utf-8', newline='') as fm:
        csv.writer(fm).writerow([name, age])
    return jsonify({'success': True})

@app.route('/save_car', methods=['POST'])
def save_car_def():
    data = request.get_json()
    name = data['name']
    plate = data['plate']
    
    # Сохранение данных в cars.csv
    with open('csvfiles/cars.csv', 'a', encoding='utf-8', newline='') as fc:
        csv.writer(fc).writerow([name, plate])
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)