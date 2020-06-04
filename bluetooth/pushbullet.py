import requests
import json

def send_notification(title, message, token):

    data_send = {"type": "note", "title": title, "body": message}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + token, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        return "Something Wrong"
    else:
        return "Notification sent"