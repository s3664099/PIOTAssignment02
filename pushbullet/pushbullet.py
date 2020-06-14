"""
.. module:: pushbullet

"""
import requests
import json

#Method to send a push bullet notification
#The method takes a title, a message, and the token
#The token is stored in the database and relates to the engineer assigned the tasl
#The message comprises of othe details of the vehicle
def send_notification(title, message, token):
    """
    Send notifications

    """
	#Constructs the json file for push bullet
    data_send = {"type": "note", "title": title, "body": message}

	#Calls the pushbullet API to send the message 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + token, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        return "Something Wrong"
    else:
        return "Notification sent"