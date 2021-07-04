from os import name
from flask import Flask,render_template,request,redirect
#from werkzeug.utils import redirect

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html', name='hello welcome to my web app')


def database(data):
    with open('data.txt',mode='a+') as file:
        file.writelines(f'\n{data["name"]},{data["email"]},{data["message"]}')



@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        database(data)
        name = data['name']
        return redirect('/#submit')
    else:
        return 'something went wrong'