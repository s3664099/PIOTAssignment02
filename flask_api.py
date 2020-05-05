import pymysql,datetime
from pymysql.cursors import DictCursor
from flask import Flask, Blueprint, request, jsonify, render_template,session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import app
from login import verify_password
import os, requests, json
from database_utils import databaseUtils
from flask import current_app as app
from decimal import Decimal

api = Blueprint("api", __name__)

#db = SQLAlchemy()
ma = Marshmallow()

# Declaring the model.
db_hostname = '35.197.174.1'
db_username = 'root'
db_password = 'password'
database = 'car_app_db'

print("Connecting")
# The main function. The database is opened, and the functions are executed
myConnection = pymysql.connect(host=db_hostname, user=db_username, passwd=db_password, db=database, charset='utf8mb4')

print("*********")
print("Connected")
cur = myConnection.cursor(DictCursor)
cur.execute('SET NAMES utf8mb4')
cur.execute('SET CHARACTER SET utf8mb4')
cur.execute('SET character_set_connection=utf8mb4')
cur.close()

dbObj=databaseUtils(db_hostname,db_username,db_password,database)

"""class user(db.Model):
    __tablename__ = "user"
    username = db.Column(db.Text, primary_key = True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text,unique = True)
    # Username = db.Column(db.String(256), unique = True)

    def __init__(self, firstname,lastname,email,password, username = None):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = email

class UserSchema(ma.Schema):
    # Reference: https://github.com/marshmallow-code/marshmallow/issues/377#issuecomment-261628415
    def __init__(self, strict = True, **kwargs):
        super().__init__(**kwargs)
    
    class Meta:
        # Fields to expose.
        fields = ("username", "firstname","lastname","email","password")

userSchema = UserSchema()
usersSchema = UserSchema(many = True)"""

# Endpoint to show all people.
@api.route("/user", methods = ["GET"])
def getTest():
    cur=myConnection.cursor()
    cur.execute('SELECT * FROM user')
    users=cur.fetchall()
    print(users)
    cur.close()
    return jsonify(users)

# Endpoint to get person by id.
@api.route("/login/<email>", methods = ["GET"])
def getLogin(email):
    cur=myConnection.cursor()
    cur.execute('Select email, password from user where email= %s',email)
    rows=cur.fetchall()
    for row in rows:
        result = json.dumps(row[1])
        if result:
            cur.close()
            return jsonify(result)
    cur.close()
    return jsonify(rows)


@api.route("/orderhistory/<email>", methods = ["GET"])
def getOrderHistory(email):
    
    cur=myConnection.cursor(DictCursor)
    cur.execute('Select username from user where email= %s',email)
    rows = cur.fetchall()
    json_data=[]
    for result in rows:
        json_data.append(dict(result))
        print(result)
        username=result["username"]
    rows=dbObj.get_booking_history(username)
    print("\n\n from booking history")
    print(rows)
    print("\n\n")
    if rows:
        orderhistory=json.dumps(rows,default=decimal_default)
        orderhistory=json.loads(orderhistory)
        cur.close()
        return jsonify(orderhistory)
    cur.close()
    return jsonify(rows)

@api.route("/cars",methods=['GET'])
def getCars():
    cur=myConnection.cursor(DictCursor)
    cur.execute("Select * from car")
    rows=cur.fetchall()
    availablecars=json.dumps(rows,default=decimal_default)
    availablecars=json.loads(availablecars)
    cur.close()
    return jsonify(availablecars)

@api.route("/searchcar/<search>",methods=['GET'])
def searchCars(search):
    carList=dbObj.return_vehicle_details(search)
    carList=json.dumps(carList,default=decimal_default)
    carList=json.loads(carList)
    return jsonify(carList)
    """cur=myConnection.cursor(DictCursor)
    cur.execute("Select * from car where rego= %s",search)
    rows=cur.fetchall()
    if rows:
        carList=json.dumps(rows,default=decimal_default)
        carList=json.loads(carList)
        cur.close()
        return jsonify(carList)
    else:
        cur.execute("Select * from car where make= %s",search)
        rows=cur.fetchall()
        if rows:
            carList=json.dumps(rows,default=decimal_default)
            carList=json.loads(carList)
            cur.close()
            return jsonify(carList)
        else:
            cur.execute("Select * from car where model= %s",search)
            rows=cur.fetchall()
            if rows:
                carList=json.dumps(rows,default=decimal_default)
                carList=json.loads(carList)
                cur.close()
                return jsonify(carList)
            else:
                cur.execute("Select * from car where color= %s",search)
                rows=cur.fetchall()
                if rows:
                    carList=json.dumps(rows,default=decimal_default)
                    carList=json.loads(carList)
                    cur.close()
                    return jsonify(carList)
    return jsonify(rows)"""

def decimal_default(obj):
    if isinstance(obj,Decimal):
        return float(obj)
    if isinstance(obj, datetime.datetime):
        return obj.__str__()
    raise TypeError


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# Endpoint to create new person.
"""@api.route("/person", methods = ["POST"])
def addPerson():
    name = request.json["name"]
 
    newPerson = Person(Name = name)

    db.session.add(newPerson)
    db.session.commit()

    return personSchema.jsonify(newPerson)

# Endpoint to update person.
@api.route("/person/<id>", methods = ["PUT"])
def personUpdate(id):
    person = Person.query.get(id)
    name = request.json["name"]

    person.Name = name

    db.session.commit()

    return personSchema.jsonify(person)

# Endpoint to delete person.
@api.route("/person/<id>", methods = ["DELETE"])
def personDelete(id):
    person = Person.query.get(id)

    db.session.delete(person)
    db.session.commit()

    return personSchema.jsonify(person) """
