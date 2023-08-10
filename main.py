from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import select
import os
import requests
from datetime import datetime

app = Flask(__name__)

# @app.route("/", methods=['GET'])
# def home():
#     return jsonify({
#         'msg':'Welcome to the first flask page',
#         'name': 'Vishaal Nair'
#     })

URL = "https://dummyjson.com/users/"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'db,sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

with app.app_context():
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(15),unique=True)
    birth_date = db.Column(db.String(10))

    def __init__(self,first_name,last_name,age,gender,email,phone,birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone
        self.birth_date = birth_date

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id','first_name','last_name','age','gender','email','phone','birth_date')
        #model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)


#Add new User
@app.route('/adduser',methods=['POST'])
def addUser():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    age = request.json['age']
    gender = request.json['gender']
    email = request.json['email']
    phone = request.json['phone']
    birth_date = request.json['birth_date']

    newUser = User(first_name,last_name,age,gender,email,phone,birth_date)
    db.session.add(newUser)
    db.session.commit()
    return user_schema.jsonify(newUser)


#Show all users
@app.route('/getalluser',methods=['GET'])
def GetAllUser():
    allUsers = User.query.all()
    result = users_schema.dump(allUsers)
    return jsonify(result)

#get Users
@app.route('/api/users/<string:firstName>/',methods=['GET'])
def getUsers(firstName):
    users = User.query.filter(User.first_name.contains(firstName)).all()
    if users:
        return jsonify([user_schema.dump(user) for user in users])
    
    response = requests.get(URL+"search?q="+firstName)
    data = response.json()
    newUsers = []
    results = {"users":[]}
    for user in data["users"]:
        if user["firstName"].__contains__(firstName):
            first_name = user["firstName"]
            last_name = user["lastName"]
            age = user["age"]
            gender = user["gender"]
            email = user["email"]
            phone = user["phone"]
            birth_date = user["birthDate"]
            newUser = User(first_name,last_name,age,gender,email,phone,birth_date)
            newUsers.append(newUser)
            results["users"].append(user_schema.dump(newUser))
    
    db.session.add_all(newUsers)
    db.session.commit()

    return results



if __name__=='__main__':
    app.run(debug=True,port=5000)