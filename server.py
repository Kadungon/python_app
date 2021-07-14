from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
import os

connection_string = os.environ['SQL_SERVER']
#connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=db29.database.windows.net;DATABASE=kadudb;UID=azuredb;PWD=Tallman@2222"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customer'
    CustomerId = db.Column(db.Integer,primary_key=True)
    CustomerName = db.Column(db.String(100))
    Email = db.Column(db.String(50))
    CustomerMessage = db.Column(db.String(100))

    def __init__(self,CustomerName,Email,CustomerMessage):
        self.CustomerName = CustomerName
        self.Email = Email
        self.CustomerMessage = CustomerMessage


@app.route('/')
def home_page():
    return render_template('index.html', name=os.environ['NAME'])

@app.route('/profile')
def info_page():
    data = Customer.query.all()
    return render_template('data.html', form=data)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = Customer(data["name"],data["email"],data["message"])
        db.create_all()
        db.session.add(user)
        db.session.commit()
        return redirect('/#submit')
    else:
        return 'something went wrong'