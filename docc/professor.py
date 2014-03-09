'''


@author: rohit
'''
from data.storage import Storage
import traceback

class Professors(object): 
    
    def __init__(self):
        print 'Professor created\n'
        # create storag
        self.__store = Storage()
        
  
    def addProfessor(self, data):
        print 'In Professor.add method'
        try:
            self.__store.add('professor', data)
            return 'success'
        except:
            return 'failed'
            
    def getProfessor(self, value):
        print 'In Professor.get method'
        try:
            return self.__store.get('professor', 'username', value)
        except:
            return 'failed'
    
    def getAll(self):
        print 'In Professors.getAll method'
        try:
            return self.__store.getAll('Professor')
        except:
            return 'failed'
        
    def updateProfessor(self, value, data):
        print 'In Professor.update method'
        try:
            return self.__store.update('Professor', 'email', value, data)
        except:
            return 'failed'
    
    def updateProfessorOwnCourse(self, email, courseid):
        print 'In Course.updateProfessorOwnCourse method'
        try:
            return self.__store.addProfessorOwnCourse(email, courseid)
        except:
            traceback.print_exc()
            return 'failed'
            
    def removeProfessor(self, value):
        print 'In Professor.remove method'
        try:
            return self.__store.remove('Professor', 'email', value)
        except:
            return 'failed' 