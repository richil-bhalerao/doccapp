'''


@author: roopak
'''
from data.storage import Storage
import traceback

class Users(object): 
    
    def __init__(self):
        print 'User created\n'
        # create storag 
        self.__store = Storage()
        
  
    def addUser(self, data):
        print 'In User.add method'
        try:
            self.__store.add('user', data)
            return 'success'
        except:
            return 'failed'
            
    def getUser(self, value):
        print 'In User.get method'
        try:
            return self.__store.get('user', 'email', value)
        except:
            return 'failed'
    
    def getAll(self):
        print 'In Users.getAll method'
        try:
            return self.__store.getAll('user')
        except:
            return 'failed'
        
    def updateUser(self, value, data):
        print 'In User.update method'
        try:
            return self.__store.update('user', 'email', value, data)
        except:
            return 'failed'
    
    def updateUserOwnCourse(self, email, courseid):
        print 'In Course.updateUserOwnCourse method'
        try:
            return self.__store.addUserOwnCourse(email, courseid)
        except:
            traceback.print_exc()
            return 'failed'
            
    def removeUser(self, value):
        print 'In User.remove method'
        try:
            return self.__store.remove('user', 'email', value)
        except:
            return 'failed' 