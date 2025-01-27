from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import csv
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)


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



@app.route('/save_mechanic', methods=['POST'])
def save_mechanic():
    data = request.get_json()
    mechanics = read_csv('csvfiles/mechanics.csv')
    mechanics.append(data)
    write_csv('csvfiles/mechanics.csv', mechanics)
    return jsonify({'success': True})

    # Сохранение данных в mechanics.csv
    with open('csvfiles/mechanics.csv', 'a', encoding='utf-8', newline='') as fm:
        csv.writer(fm).writerow([name, age])
    return jsonify({'success': True})

@app.route('/save_car', methods=['POST'])
def save_car():
    data = request.get_json()
    cars = read_csv('cars.csv')
    cars.append(data)
    write_csv('cars.csv', cars)
    return jsonify({'success': True})

    # Сохранение данных в cars.csv
    with open('csvfiles/cars.csv', 'a', encoding='utf-8', newline='') as fc:
        csv.writer(fc).writerow([name, plate])
    return jsonify({'success': True})


def read_csv(filename):
    try:
        df = pd.read_csv(filename)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        logging.warning(f"File {filename} not found. Creating an empty DataFrame with headers.")
        if filename == 'mechanics.csv':
            df = pd.DataFrame(columns=['Name', 'Age'])
        elif filename == 'cars.csv':
            df = pd.DataFrame(columns=['Name', 'Number'])
        return df.to_dict(orient='records')
    except pd.errors.EmptyDataError:
        logging.warning(f"File {filename} is empty. Creating an empty DataFrame with headers.")
        if filename == 'mechanics.csv':
            df = pd.DataFrame(columns=['Name', 'Age'])
        elif filename == 'cars.csv':
            df = pd.DataFrame(columns=['Name', 'Number'])
        return df.to_dict(orient='records')
    except Exception as e:
        logging.error(f"Error reading {filename}: {e}")
        return []


def write_csv(filename, data):
    try:
        if not data:
            # Если список пустой, создаем новый CSV файл с заголовками
            if filename == 'mechanics.csv':
                df = pd.DataFrame(columns=['Name', 'Age'])
            elif filename == 'cars.csv':
                df = pd.DataFrame(columns=['Name', 'Number'])
        else:
            df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
    except Exception as e:
        logging.error(f"Error writing to {filename}: {e}")


@app.route('/delete_mechanic', methods=['POST'])
def delete_mechanic():
    data = request.get_json()
    mechanics = read_csv('csvfiles/mechanics.csv')
    mechanics_df = pd.DataFrame(mechanics)
    mechanics_df = mechanics_df[mechanics_df['Name'] != data.get('name')]
    write_csv('csvfiles/mechanics.csv', mechanics_df.to_dict(orient='records'))
    return jsonify({'success': True})

@app.route('/delete_car', methods=['POST'])
def delete_car():
    data = request.get_json()
    cars = read_csv('cars.csv')
    cars_df = pd.DataFrame(cars)
    cars_df = cars_df[cars_df['Number'] != data.get('plate')]
    write_csv('cars.csv', cars_df.to_dict(orient='records'))
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)