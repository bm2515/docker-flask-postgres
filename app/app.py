from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time


DBUSER = 'postgres'
DBPASS = 'test123'
DBHOST = 'localhost'
DBPORT = '5432'
DBNAME = 'SIHA_postgres'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.String(50))
    sex = db.Column(db.String(50))
    height = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    diabetes = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default= datetime.now)
    
    fitness = db.relationship('Fitness', backref= 'user', lazy = True)

    def __init__(self, username, first_name, last_name, age, sex, height, weight, diabetes):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.height = height
        self.weight = weight
        self.diabetes = diabetes



class Fitness(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    steps = db.Column(db.String(50))
    calories = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default= datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __init__(self, first_name, last_name, steps, calories, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.steps = steps
        self.calories = calories
        self.user_id = user_id



class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))

    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr


def database_initialization_sequence():
    db.create_all()
    test_rec = User(
        "corey_34",
        "Corey",
        "Schafer",
        "22",
        "Male",
        "170cm",
        "70kg",
        "No")

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        req_data = request.get_json()

        username = req_data["user_name"]
        user_first_name = req_data["first_name"]
        user_last_name = req_data["last_name"]
        age = req_data["Age"]
        sex = req_data["Sex"]
        height = req_data["Height"]
        weight = req_data["Weight"]
        diabetes = req_data["Diabetes"]

        user = User(username, user_first_name, user_last_name, age, sex, height, weight, diabetes)
        db.session.add(user)
        db.session.commit()
    
        return jsonify(req_data)

    else:
        return '''<h1>
        Enter your user credentials to register with the system
        </h1>'''




@app.route("/<usr>", methods=["POST", "GET"])
def user(usr):

    if request.method == "POST":
        
        req_data = request.get_json()


        user = User.query.filter_by(username=usr).first()

        user_first_name = req_data["first_name"]
        user_last_name = req_data["last_name"]
        steps = req_data['steps']
        calories = req_data['calories']
        user_id = user.id


        fitness_data = Fitness(user_first_name, user_last_name, steps, calories, user_id)
        db.session.add(fitness_data)
        db.session.commit()

        return jsonify(req_data)

    else:
            
        return '''<h1>
        Enter your Fitness credentials to register at the system
        </h1>'''


if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')
