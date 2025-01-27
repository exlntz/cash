from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import pandas as pd


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_def():
    return render_template('home/home.html')



@app.route('/atm')  #Automated teller machine
def atm_def():
    return render_template('atms/atm.html')



@app.route('/maps')
def maps_def():
    return render_template('maps/maps.html')





@app.route('/admin')
def admin_def():
    # Загрузка данных из CSV файлов
    mechanics_csv = pd.read_csv('csvfiles/mechanics.csv').to_dict(orient='records')
    print(mechanics_csv)
    cars_csv = pd.read_csv('csvfiles/cars.csv').to_dict(orient='records')
    print(cars_csv)
    return render_template('/admin/admin.html', mechanics=mechanics_csv, cars=cars_csv)


@app.route('/save_mechanic', methods=['POST'])
def save_mechanic():
    name = request.form['mechanicName']
    age = request.form['mechanicAge']
    
    # Сохранение данных в mechanics.csv
    with open('csvfiles/mechanics.csv', 'a',encoding='utf-8',newline='') as fm:
        csv.writer(fm).writerow([name,age])

    return f'механику добавлен'



@app.route('/save_car', methods=['POST'])
def save_car_def():
    name = request.form.get('carName')
    plate = request.form.get('carPlate')
    
    # Сохранение данных в cars.csv
    with open('csvfiles/mechanics.csv', 'a', encoding='utf-8', newline='') as fc:
        csv.writer(fc).writerow([name, plate])

    return f'механик успешно добавлен'









#@app.route('templates/admin/admin.html', methods=['POST'])
def submit():
    # Получаем слово из формы
    name_atm = request.form.get('name1','Ошибка')
    age_atm = request.form.get('age1','Ошибка')
    with open('csvfiles/mechanics.csv','a',encoding='utf-8',newline='') as fm:
        csv.writer(fm).writerow([name_atm,age_atm])
    return f'Механик успешно добавлен!'



#@app.route('/submit_mechanic', methods=['POST'])
def submit():
    # Получаем слово из формы
    name_mechanic = request.form.get('name2','Ошибка')
    age_mechanic = request.form.get('age2','Ошибка')
    with open('csvfiles/mechanics.csv','a',encoding='utf-8',newline='') as fm:
        csv.writer(fm).writerow([name_mechanic,age_mechanic])
    return f'Механик успешно добавлен!'



#@app.route('/submit_car', methods=['POST'])
def submit():
    # Получаем слово из формы
    name_car = request.form.get('name','Ошибка')
    age_car = request.form.get('age','Ошибка')
    with open('csvfiles/mechanics.csv','a',encoding='utf-8',newline='') as fm:
        csv.writer(fm).writerow([name_car,age_car])
    return f'Механик успешно добавлен!'



if __name__ == '__main__':
    app.run(debug=True)
