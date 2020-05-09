import pymysql,datetime
from pymysql.cursors import DictCursor
from flask import Flask, Blueprint, request, jsonify, render_template,session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import app
from login import verify_password,hash_password,logon
import os, requests, json
from database_utils import databaseUtils
from flask import current_app as app
from decimal import Decimal
from datetimeconverter import convertdatetime



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
cur = myConnection.cursor()
cur.execute('SET NAMES utf8mb4')
cur.execute('SET CHARACTER SET utf8mb4')
cur.execute('SET character_set_connection=utf8mb4')
cur.close()

dbObj=databaseUtils(db_hostname,db_username,db_password,database)
#Endpoint to create a new user
@api.route("/registeruser", methods = ["POST"])
def getTest():
    password=hash_password(request.json['password'])
    response=dbObj.insert_user(request.json['username'],request.json['firstname'],request.json['lastname'],password,request.json['email'])
    print("\n\nThis is in register\n\n")
    print(response)
    if response=='success':
        return jsonify(response)
    else:
        return jsonify(response)
        

@api.route("/login", methods = ["POST"])
def getLogin():
    result=logon(request.json['email'],request.json['password'])
    return jsonify(result)


@api.route("/orderhistory/<email>", methods = ["GET"])
def getOrderHistory(email):
    rows=dbObj.get_booking_history(email)
    if rows:
        orderhistory=json.dumps(rows,default=decimal_default)
        orderhistory=json.loads(orderhistory)
        return jsonify(orderhistory)
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

#@api.route("/booking",methods=['POST'])
#def getBooking():
#session['email'] for inserting into booking
#write a booking.py to calculate or validate if needed , but check database_utils if code can be reused.
#insert into booking

@api.route("/searchcar/<search>",methods=['GET'])
def searchCars(search):
    carList=dbObj.return_vehicle_details(search)
    carList=json.dumps(carList,default=decimal_default)
    carList=json.loads(carList)
    return jsonify(carList)


@api.route("/bookcar", methods = ["POST"])
def bookcar():
    pickup=convertdatetime(request.json['pickup'])
    dropoff=convertdatetime(request.json['dropoff'])
    cost="{:.2f}".format(15.00)
    response=dbObj.book_vehicle(request.json['email'],request.json['rego'],pickup,dropoff)
    if response=='Vehicle already booked':
        return jsonify(response)
    else:
        return jsonify(response)



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
