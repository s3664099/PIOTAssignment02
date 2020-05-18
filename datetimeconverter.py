from datetime import datetime
def convertdatetime(Input):
    result = datetime.strptime(Input,'%Y-%m-%d %H:%M:%S.%f')
    return result

def convertdatetimeforinsert(Input):
    result = datetime.strptime(Input,'%Y-%m-%dT%H:%M')
    return result