"""
Storage interface
"""

import time, json
#Ric Start
import traceback
from pymongo import Connection
from json import JSONEncoder
from bson.objectid import ObjectId
#Ric End

class Storage1(object):
    
    #Initialize db object to none
    db = None 
    
    def __init__(self):
       # initialize our storage, data is a placeholder
       self.data = {}
       # for demo
       self.data['created'] = time.ctime()
       
       #Ric Start
       connection = Connection('localhost', 27017)
       #Create db object only if it is not created 
       if self.db is None:
           self.db = connection.test
       #Ric End
    
    
    #######################################Ric Start############################################
    def add(self, collection, data):
        print 'In Storage.add method'
        try:
            return self.db[collection].save(data)
            print 'data added in moocdb'
        except:
            traceback.print_exc() 
            return "Error: Data cannot be added"
    
    def get(self, collection, fieldname, value):
        print 'In Storage.get method'
        try:
            return self.db[collection].find_one({fieldname:value}) #, {'_id':0})
        except:
            traceback.print_exc() 
            return "Error: Data cannot be retrieved"
        
    def update(self, collection, fieldname, value, data):
        print 'In Storage.update method'
        try:
            self.db[collection].update({fieldname:value}, data);
        except:
            traceback.print_exc() 
            return "Error: Data cannot be updated"    
    
    def remove(self, collection, fieldname, value):
        print 'In Storage.remove method'
        try:
            self.db[collection].remove({fieldname:value})
        except:
            traceback.print_exc() 
            return "Error: Data cannot be deleted"
    
    def getAll(self, collection):
        print 'In Storage.getAll method'
        try:
            return self.db[collection].find_one() #{}, {'_id':0, 'date':0})
        except:
            traceback.print_exc() 
            return "All data cannot be retrieved" 
    


try:
    connection = Connection('localhost', 27017)
    db = connection.test
    data = db['test'].find_one()
    
    #Get 4 values that u need in 4 variables
    thisyear = data["mobile_users"]["this_year"]
    lastyear = data["mobile_users"]["last_year"]
    yoy = data["mobile_users"]["yoy"]
    date1 = data['date']            # this is of type datetime.datetime
    date1 = date1.strftime('%m/%d/%Y')

    # Create a json payload that u need
    response = {"mobile_users": { "this_year": thisyear, "last_year": lastyear, "yoy": yoy, "date": date1} }

    #Now to remove the unicode symbol use
    response = json.dumps(response)
    print response
except:
    traceback.print_exc()
