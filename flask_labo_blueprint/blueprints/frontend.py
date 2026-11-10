from flask import Blueprint, render_template, request, redirect, url_for, current_app

app = Blueprint('fe', __name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/vr-shooter')
def vr_shooter():
    player_name = request.args.get('player', 'VR_Hunter')
    return render_template('vr_shooter.html', player_name=player_name)

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/products')
def prods():
    return "many things to buy"

@app.route('/hello', methods=['GET', 'POST'])
def hello_anonymous():
    if request.method == 'GET':
        return render_template('hello_form.html')
    if request.method == 'POST':
        current_app.logger.info(f'form data: {request.form}')
        input_name = request.form.get('name', 'DEFAULT_VALUE')
        return redirect(url_for('fe.hello', name=input_name))

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)
