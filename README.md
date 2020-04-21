# PIoT Assignment 02

#Database Structure
car: rego, make, model, locationLong, locationLat, colour (Primary: rego), (Foreign: make, model - makemodel)
makemodel: make, model, bodytype (Primary: make, model), (Foreign: bodytype - bodytype)
bodytype: bodytype, seats, hourlyPrice, icon (Primary: bodytype)
user: username, firstname, lastname, password, email (Primary: username)
booking: bookingnumber, rego, user, pickuptime, dropofftime, totalcost






