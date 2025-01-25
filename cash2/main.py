from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/atm')  #Automated teller machine
def atm():
    return render_template('atm.html')


@app.route('/maps')
def maps():
    return render_template('maps.html')


if __name__ == '__main__':
    app.run(debug=True)
