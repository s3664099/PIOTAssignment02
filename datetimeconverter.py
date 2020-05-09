from datetime import datetime

def convertdatetime(Input):
    result = datetime.strptime(Input, '%Y-%m-%dT%H:%M')
    return result