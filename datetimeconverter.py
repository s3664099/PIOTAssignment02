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
    Convert date and time for insert
    
    """
    result = datetime.strptime(Input,'%Y-%m-%dT%H:%M')
    return result