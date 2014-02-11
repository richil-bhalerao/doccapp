'''
Created on Apr 24, 2013

@author: rbhalerao
'''

from data.storage import Storage
import traceback
from bson.objectid import ObjectId

class Course(object):
    
    def __init__(self):
        print 'Course created\n'
        # create storag 
        self.__store = Storage()
        
    
    def add(self, email, data):
        print 'In Course.add method'
        try:
            courseid = self.__store.add('course', data)
            #Also update 'own' field of user collection
            self.__store.addUserOwnCourse(email, str(courseid))
            
            return courseid 
        except:
            traceback.print_exc()
            return 'failed'
        
    def get(self, value):
        print 'In Course.get method'
        try:
            return self.__store.get('course', '_id', ObjectId(value))
        except:
            traceback.print_exc()
            return 'failed'
    
    def update(self, value, data):
        print 'In Course.update method'
        try:
            return self.__store.update('course', '_id', ObjectId(value), data)
        except:
            traceback.print_exc()
            return 'failed'    
        
    def remove(self, value):
        print 'In Course.remove method'
        try:
            return self.__store.remove('course', '_id', ObjectId(value))
        except:
            traceback.print_exc()
            return 'failed'
    
    def getAll(self):
        print 'In Course.getAll method'
        try:
            return self.__store.getAll('course')
        except:
            traceback.print_exc()
            return 'failed'
    
    def enroll(self, email, courseid):
        print 'In Course.enroll method'
        try:
            return self.__store.enrollCourse(email, courseid)
        except:
            traceback.print_exc()
            return 'failed'
        
    def drop(self, email, courseid):
        print 'In Course.drop method'
        try:
            return self.__store.dropCourse(email, courseid)
        except:
            traceback.print_exc()
            return 'failed'
    