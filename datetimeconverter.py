"""
.. module:: datetimeconverter

"""
from datetime import datetime

def convertdatetime(Input):
    """
    Convert date and time

    """
    result = datetime.strptime(Input,'%Y-%m-%d %H:%M:%S.%f')
    return result

def convertdatetimeforinsert(Input):
    """
    Insert date and time conversion

    """
    result = datetime.strptime(Input,'%Y-%m-%dT%H:%M')
    return result