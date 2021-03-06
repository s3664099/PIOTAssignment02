# PIoT Assignment 03

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

**Instructions**:
- Ensure Python3.3 or later is installed.
- Navigate to main project folder in Terminal/Cmd. (alternatively open project in VScode and use Terminal there)
- Enter "pip install -r requirements.txt" to install all required packages.
- Enter "python3 flask_main.py" to run the application.
- API calls for map in the JavaScript files in static folder and the agentpi and master pi files need to be modified during setup.
- These calls need to be made to the specific host name of the server where the flask app is running.
- For instance: if flask is running on 10.0.0.1 then all api calls being made need to change from 127.0.0.1 to 10.0.0.1


## Project Features

**For customers**: The customers can register, logging in, search and book a car on the web-based system in MASTER PI (MP).

1. The user registration on MP is required for the first-time user. In the home page of the web-based application provides only two options:

- registration
- log in

2. Upon registration the details are stored in cloud database.

3. Upon logging in, the user is now presented with another page including following functions:

- List of available cars will be shown, such as the detailed information of cars in the list such as Make, Body Type, Colour, Seats, Location, Cost per hour.
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

**For manager**: The manager can login to the website and capture key information by looking at the visualisation dashboard.

1. Upon logging in, a dashboard webpage will be shown. In the dashboard webpage, there will be 3 types of visualisation graph.

2. The first graph is a combo bar chart where it will show the results of total comfirmed booking and cancelled the booking from our application.

3. Second graph shows the results of the percentage of frequent booked car where we will know which car brand/model has been booked the most or more likely the most favorable car for our customers to book.

4. Lastly, the third graph is a line chart where give us our day to day profit sales result.

**For engineer**: The engineers take responsibility to repair the reported cars. They will receive anotification via email once admin reported a car that is needed to be repaired. After that, the engineer can login to the system to check outand find the car’s location.

1. The engineer is able to:
- Login 
- Check the reported car’s location in the web page

2. The car will be unlocked automatically when the engineer close to the car (you will be asked toutilise Bluetooth ID to solve this problem).

3. The AP attached in the car will have the ability to detect QR code carried by engineers in order to retrieve their personal information, which will help company to know who has done what.

**Usernames and Passwords**
Engineer: engineer@phase2.com/Password1
Admin: admin@phase2.com/Password1
Manager: manager@phase2.com/Password1


## Github Repository Usage

![1](https://user-images.githubusercontent.com/62014219/84592506-8d253580-ae89-11ea-8d7b-bccacfdc796c.PNG)

![2](https://user-images.githubusercontent.com/62014219/84592496-88f91800-ae89-11ea-8aa5-a3a6f76f792f.PNG)

![3](https://user-images.githubusercontent.com/62014219/84592499-8ac2db80-ae89-11ea-8ad2-18840b9cbeee.PNG)

![4](https://user-images.githubusercontent.com/62014219/84592500-8ac2db80-ae89-11ea-9b88-f45ffd08c4b0.PNG)

![5](https://user-images.githubusercontent.com/62014219/84592502-8b5b7200-ae89-11ea-90a3-8e7ee3888861.PNG)

![6](https://user-images.githubusercontent.com/62014219/84592503-8bf40880-ae89-11ea-8fa5-2315c9c7a56a.PNG)

![7](https://user-images.githubusercontent.com/62014219/84592504-8c8c9f00-ae89-11ea-8989-f6fbd09d68cf.PNG)

![8](https://user-images.githubusercontent.com/62014219/84592505-8c8c9f00-ae89-11ea-8598-998c78af9eab.PNG)

## Trello Board Usage

![9](https://user-images.githubusercontent.com/62014219/84592526-a7f7aa00-ae89-11ea-9bb4-a91d7896111c.PNG)

![10](https://user-images.githubusercontent.com/62014219/84592524-a62de680-ae89-11ea-9f77-a54b1b1a4303.PNG)

