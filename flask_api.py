"""
.. module:: flask_api

"""
import json
from decimal import Decimal

import datetime
import pymysql
from flask import Blueprint, request, jsonify

from Database.database_utils import databaseUtils
from datetimeconverter import convertdatetimeforinsert
from login import hash_password, hashing_password, login

api = Blueprint("api", __name__)

# Declaring the model
# This should be in a config.json file, and the 
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

#The DB is being connected to twice, it should only be once, and called through the singleton method
dbObj=databaseUtils(db_hostname,db_username,db_password,database)

#Endpoint to create a new user
@api.route("/registeruser", methods = ["POST"])
def registerUser():
    """
    User registration

    """
    password=hash_password(request.json['password'])
    response=dbObj.insert_user(request.json['username'],request.json['firstname'],request.json['lastname'],password,request.json['email'])
    if response=='success':
        return jsonify(response)

@api.route("/registeremployee", methods=['POST'])
def registerEmplyee():
    password=hash_password(request.json['password'])
    response=dbObj.create_employee(request.json['username'],request.json['firstname'],request.json['lastname'],password,request.json['email'],request.json['role'])
    return jsonify(response)

#Login Endpoint
@api.route("/login", methods = ["POST"])
def Login():
    """
    User login

    """

    #The connection is being sent through, this should by dbObj
    result=login(request.json['email'],request.json['password'],myConnection)
    if result==2:
        response="success"
    elif result==3:
        response="password incorrect"
    else:
        response="username incorrect"

    return jsonify(response)
    
#validates if the user account exists in MP and if the user has a valid booking
@api.route("/validate",methods=["POST"])
def validateUserAndBooking():
    """
    Validation of user and booking

    """
    response="Not found"

    #Once again, the dbObj should be sent through
    result=login(request.json['email'],request.json['password'],myConnection)
    if result == 2:

        #Confirms the booking
        booking =dbObj.get_confirmed_booking_for_user(request.json['email'],request.json['rego'],request.json['date_time'])
        if "<!DOCTYPE" not in booking:
            if booking:
                for row in booking:

                    #If the booking is confirmed then the status is updated
                    result=dbObj.change_booking_status(row['bookingnumber'],"ACTIVE")
                    if result == "Success":
                        response= "Success"
                    else:
                        response=result
            else:

                #If no specific booking is found, then all active bookings are searched for.
                checkActiveBooking=dbObj.get_active_booking_for_user(request.json['email'],request.json['rego'])
                if checkActiveBooking:
                    response="Car Already Unlocked"
                    return jsonify(response)
                response= "Booking Not Found"
        else:
            response="Credentials not found"
    
    return jsonify(response)

#validates if the user account exists in MP and if the user has a valid booking
@api.route("/validateUser",methods=["POST"])
def validateUserBooking():
        #Confirms the booking
        response="Booking Not Found"
        booking =dbObj.get_confirmed_booking_for_user(request.json['email'],request.json['rego'],request.json['date_time'])
        if "<!DOCTYPE" not in booking:
            if booking:
                for row in booking:

                    #If the booking is confirmed then the status is updated
                    result=dbObj.change_booking_status(row['bookingnumber'],"ACTIVE")
                    if result == "Success":
                        response= "Success"
                    else:
                        response=result
            else:

                #If no specific booking is found, then all active bookings are searched for.
                checkActiveBooking=dbObj.get_active_booking_for_user(request.json['email'],request.json['rego'])
                if checkActiveBooking:
                    response="Car Already Unlocked"
                    return jsonify(response)
                response= "Booking Not Found"
        else:
            response="Credentials not found"
    
        return jsonify(response)

#Updates the availability of a car to 0 which means unavailable
@api.route("/updatecarstatus",methods=["POST"])
def updateCarStatus():
    """
    Updates of vehicle status

    """
    result=dbObj.update_availability(request.json['rego'],0)
    return result

#This function is for returning the car. The booking status to taken, and the updated when found.
@api.route("/returncar",methods=["POST"])
def returnCar():
    """
    Returning vehicle

    """
    result=dbObj.get_active_booking_for_user(request.json['email'],request.json['rego'])
    if "<!DOCTYPE" not in result:
        for row in result:
            update=dbObj.change_booking_status(row['bookingnumber'],"COMPLETED")
            if update=="Success":
                updatecar=dbObj.update_availability(request.json['rego'],1)
                return jsonify(updatecar)
    return jsonify("Could not complete return")

#This method returns the username based upon a submitted email
@api.route("/username/<email>",methods=["GET"])
def getUsername(email):
    """
    Get the username

    """
    rows=dbObj.return_user_details(email)
    if rows:
        for row in rows:
            user=json.dumps(row['username'],default=decimal_default)
            user=json.loads(user)
        return jsonify(user)
    return jsonify(rows)

#This method returns the booking history for the user
@api.route("/orderhistory/<email>", methods = ["GET"])
def getOrderHistory(email):
    """
    Order history

    """
    rows=dbObj.get_booking_history(email)
    if rows:
        orderhistory=json.dumps(rows,default=decimal_default)
        orderhistory=json.loads(orderhistory)
        return jsonify(orderhistory)
    return jsonify(rows)

#This method returns all of the bookings that have been confirmed
@api.route("/confirmedbookings/<email>", methods = ["GET"])
def getConfirmedBookings(email):
    """
    Confirmed bookings

    """
    rows=dbObj.get_confirmed_bookings(email)
    if rows:
        confirmedbookings=json.dumps(rows,default=decimal_default)
        confirmedbookings=json.loads(confirmedbookings)
        return jsonify(confirmedbookings)
    return jsonify(rows)

#This method hashes the password
#Note that the connection is being sent through as opposed to the dbObj
@api.route("/hashme", methods = ["POST"])
def HashedPassword():
    """
    Hash password

    """
    result=hashing_password(request.json['email'],request.json['password'],myConnection)
    return jsonify(result)

#This method cancels the booking
#not sure if the break is needed, probably should be avoided
@api.route("/cancelbooking/email=<emailid>",methods=['POST'])
def cancelBooking(emailid):
    """
    Cancel booking

    """
    for i in request.json:
        result=dbObj.cancel_booking(emailid,i)
        if result == "Error":
            break
            return jsonify(result)

    return jsonify(result)

#This method retures a list of all of the cars
@api.route("/cars",methods=['GET'])
def getCars():
    """
    List of cars

    """
    rows=dbObj.get_all_cars()
    availablecars=json.dumps(rows,default=decimal_default)
    availablecars=json.loads(availablecars)
    cur.close()
    return jsonify(availablecars)

#@api.route("/booking",methods=['POST'])
#def getBooking():
#session['email'] for inserting into booking
#write a booking.py to calculate or validate if needed , but check database_utils if code can be reused.
#insert into booking

#This method is used to search for specific cars
@api.route("/searchcar/<search>",methods=['GET'])
def searchCars(search):
    """
    Search for cars

    """
    carList=dbObj.return_vehicle_details(search)
    carList=json.dumps(carList,default=decimal_default)
    carList=json.loads(carList)
    return jsonify(carList)

#This method is used to book a vehicle
@api.route("/bookcar", methods = ["POST"])
def bookcar():
    """
    Book a vehicle

    """
    pickup=convertdatetimeforinsert(request.json['pickup'])
    dropoff=convertdatetimeforinsert(request.json['dropoff'])
    response=dbObj.book_vehicle(request.json['email'],request.json['rego'],pickup,dropoff)
    return jsonify(response)

#APIs for phase 2

@api.route("/role/<role>/<email>",methods=['GET'])
def getUserRole(role,email):
    result='Error'
    rows=dbObj.get_user_role(role,email)
    if rows:
        result='Success'
        return jsonify(result)
    return jsonify(result)

@api.route("/finduserdetails/<email>",methods=['GET'])
def getUserDetails(email):
    rows=dbObj.get_user_search(email)
    return jsonify(rows)
    

@api.route("/bookinghistory/<rego>", methods=['GET'])
def bookinghistory(rego):
    rows=dbObj.get_car_booking_history(rego)
    if rows:
        bookinghistory=json.dumps(rows,default=decimal_default)
        bookinghistory=json.loads(bookinghistory)
        return jsonify(bookinghistory)
    return jsonify(rows)

@api.route("/users", methods=['GET'])
def getUsers():
    result='No Users'
    rows=dbObj.get_all_users()
    if rows:
        return jsonify(rows)
    return jsonify(result)

@api.route("/modifyuserdetails",methods=['POST'])
def modifyuserdetails():
    rows=dbObj.update_userdetails(request.json['firstname'],request.json['lastname'],request.json['role'],request.json['status'],request.json['email'])
    return jsonify(rows)

@api.route("/findcardetails/<rego>",methods=['GET'])
def getCarDetails(rego):
    rows=dbObj.get_car_details(rego)
    if rows:
        result=json.dumps(rows,default=decimal_default)
        result=json.loads(result)
        return jsonify(result)
    else:
        return jsonify("Error")
        
@api.route("/modifycardetails",methods=['POST'])
def modifycardetails():
    rows=dbObj.update_cardetails(request.json['colour'],request.json['make'],request.json['model'],request.json['locationLat'],request.json['locationLong'],request.json['rego'])
    return jsonify(rows)

@api.route("/findengineers",methods=['GET'])
def getEngineers():
    rows=dbObj.get_engineers()
    if rows:
        return jsonify(rows)
    return "No Engineers Found"

@api.route("/createservicerequest",methods=['POST'])
def createServiceRequest():
    rows=dbObj.create_service_request(request.json['rego'],'3000',request.json['engineeremail'])
    return jsonify(rows)

@api.route("/servicehistory",methods=['GET'])
def getServiceHistory():
    rows=dbObj.get_all_service_requests()
    return jsonify(rows)
    
@api.route("/unservicedcars",methods=['GET'])
def getUnservicedCars():
    rows=dbObj.get_all_unserviced_cars()
    unservicedcars=json.dumps(rows,default=decimal_default)
    unservicedcars=json.loads(unservicedcars)
    return jsonify(unservicedcars)

@api.route("/getallcars",methods=['GET'])
def getAllCars():
    rows=dbObj.getCars()
    allcars=json.dumps(rows,default=decimal_default)
    allcars=json.loads(allcars)
    return jsonify(allcars)

@api.route("/engineerdetails",methods=['GET'])
def getEngineersDetails():
    rows=dbObj.get_engineers_details()
    if rows:
        return jsonify(rows)
    return "No Engineers Found"

@api.route("/deleteuser/<email>",methods=['GET'])
def deleteUser(email):
    rows=dbObj.delete_user(email)
    return jsonify(rows)
#A helper method to convert onjects to floats or strings to avoid conflicts with jsonify .
def decimal_default(obj):
    """
    Prevent conflicts

    """
    if isinstance(obj,Decimal):
        return float(obj)
    if isinstance(obj, datetime.datetime):
        return obj.__str__()
    raise TypeError


