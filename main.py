from flask import Flask, render_template,request
import csv


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
    return render_template('admin/admin.html')


@app.route('/admin/submit/mechanic', methods=['POST'])
def submit():
    # Получаем слово из формы
    name = request.form.get('name')
    age = request.form.get('age')
    with open('csvfiles/mechanics.csv','a',encoding='utf-8',newline='') as fm:
        csv.writer(fm).writerow([name,age])
    return f'Механик успешно добавлен!'


if __name__ == '__main__':
    app.run(debug=True)
