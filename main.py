from flask import Flask, render_template

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


@app.route('/registration')
def registration_def():
    return render_template('registration/registration.html')

#надо сделать при условии что логин и пароль админа
#если логин и пароль админа то на главной странице нужно сделать кнопку админ панель
#и уже потом перекидывать на admin.html
@app.route('/admin')
def admin_def():
    return render_template('admin/admin.html')

if __name__ == '__main__':
    app.run(debug=True)
