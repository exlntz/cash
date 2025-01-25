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



@app.route('/admin')
def admin_def():
    return render_template('admin/admin.html')


if __name__ == '__main__':
    app.run(debug=True)
