import database_utils as db

# Reference: https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
#A singleton wrapper class to prevent more than one DB connection being established
class Singleton:
    __instance = None

    #Returns a copy of the Database class
    @staticmethod
    def get_instance():
        if(Singleton.__instance == None):
            Singleton()
        return Singleton.__instance

    #Creates a copy of the class but throws an exception if more than one is
    #created
    def __init__(self, host, user, password, database):
        if(Singleton.__instance != None):
            raise Exception("You cannot create more than one connection!")
        else:
            Singleton.__instance = db.databaseUtils(host, user, password, database)

