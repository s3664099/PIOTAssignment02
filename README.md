# PIoT Assignment 02

## Bhavi Sanjay Mehta s3811346
## David Alfred Sarkies s3664099
## Jia Hong Tay s3686990
## Michael Blakebrough s3622180

**For customers**: The customers can register, logging in, search and book a car on the web-based system in MASTER PI (MP).

1. The user registration on MP is required for the first-time user. In the home page of the web-based application provides only two options:

- registration
- log in

2. Upon registration the details are stored in cloud database.

3. Upon logging in, the user is now presented with another page including following functions:

- show a list of cars available, you need to show the detailed information of cars in the list such as Make, Body Type, Colour, Seats, Location, Cost per hour.
- search for a car based on body type or other features.
- book a car based on car identity, the user will be asked to input booking details.
- cancel a booking
- logout

4. When the customer arrives at the car booked, the AgentPI (AP) provides two options available for unlocking the car:

- using console-based system which allows them to type in the user credentials or,
- using a facial recognition system

5. Upon logging in, the user’s credential will be sent from AP to MP via sockets. At the same time, MP will check the credential and send the response message back to AP. The AP will execute the operation according to the message from MP.

6. When the customer enters and leaves the booked car, the AgentPI (AP) will send messageto MP in order to change the availability of the car.