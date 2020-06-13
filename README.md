# PIoT Assignment 02

## Bhavi Sanjay Mehta s3811346
## David Alfred Sarkies s3664099
## Jia Hong Tay s3686990
## Michael Blakebrough s3622180

## Introduction
In this project, our team has to develop an automatic car share system. This systemisused to book, find and unlockand locka car. In addition, the customer can report some issues with the car to help the company to maintain the cars. The application has four types of users: customer,  company  manager,  engineers  and  system administrator.

In this project, there will be extensive use of the Google Calendar API (https://developers.google.com/calendar/v3/reference/) to work with our RaspberryPi. We will also be using Google Cloud IoT Platform (https://cloud.google.com/solutions/iot/).

In summary, the implementation of this project involves the following components:
- Writing a website application using Python’s microframework Flask
- Writing your own API using Python’s microframework Flask
- Python documentation tools such as Sphinx
- Practice third party API•Unit testing in Python
- AI features such as object-detection system
- Programming with Cloud databases•Selected Software Engineering Project Management/Tools

**Installation instructions**:
- Ensure Python3.3 or later is installed.
- Navigate to main project folder in Terminal/Cmd. (alternatively open project in VScode and use Terminal there)
- Enter "pip install -r requirements.txt" to install all required packages.
- Enter "python3 flask_main.py" to run the application.

## Project Features

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

6. When the customer enters and leaves the booked car, the AgentPI (AP) will send message to MP in order to change the availability of the car.

**For admin**: Admin can login to the website to maintain the data regarding to users and cars.

The system admin is able to:
- View car rental history
- Search users and cars
- Add, remove and modify information of users and cars
- Report car with issue, then the engineer can find and fix the problem.

**For manager**: The manager can login to the websiteandcapture key information by looking at visualisationdashboard.

1. Upon logging in,a dashboard webpage will be shown.In the dashboard webpage, there will be 3 types of visualisation graph.

2. The first graph is a combo bar chart where it will show the results of total comfirmed booking and cancelled the booking from our application.

3. Second graph shows the results of the percentage of frequent booked car where we will know which car brand/model has been booked the most or more likely the most favorable car for our customers to book.

4. Lastly, the third graph is a line chart where give us our day to day profit sales result.

**For engineer**: The engineerstake responsibility to repair the reported cars. They will receive anotification via email once admin reported a car that is needed to be repaired. After that, the engineer can login to the system to check outand find the car’s location.

1. The engineer is able to:
- Login 
- Check the reported car’s location in the web page

2. The car will be unlocked automatically when the engineer close to the car (you will be asked toutilise Bluetooth ID to solve this problem).

3. The AP attached in the car will have the ability to detect QR code carried by engineers in order to retrieve their personal information, which will help company to know who has done what.

**Usernames and Passwords**
Admin:
Manager:
Engineer:

## Github Repository Usage

## Trello Board Usage

## File Structure


