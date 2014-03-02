"""
6, Apr 2013
Last updated on 03/02/2014
"""

import time
import sys
import socket

# bottle framework
from bottle import request, response, route, run, template, abort


import traceback
from course import Course
from user import Users
from session import Session

import json
from inspect import trace
from bson.objectid import ObjectId
from json import JSONEncoder
from pymongo import *



courseobj = None
userobj = None
sessionobj = None

status = None

# A Mongo db JSON Encoder 
class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)

# Displaying welcome 
@route('/')
def root():
    cookie = request.get_cookie("session")
    print 'cookie: ', cookie
    username = sessionobj.get_username(cookie)
    if username is None:
        return 'User not logged in'
    else:
        return 'Hi and Welcome: ', username
    
   
def setup():
   print '\n**** service initialization ****\n'
   global courseobj, userobj, sessionobj 
   userobj = Users()
   courseobj = Course()
   connection = Connection('localhost', 27017)
   sessionobj = Session(connection.doccdb) 
   
   
@route('/register', method='POST')
def create_user(): 
    print 'Bottle: in create user'
    user=''
    entity = request.body.read()
    user = json.loads(entity)
    print user
    print '----'
    status = userobj.addUser(user)
    print "----"
    print status
    return status

@route('/signIn', method='PUT')
def signIn():
    print 'Checking if user exists..'
    entity = request.body.read()
    entity = json.loads(entity)
    print "username:", entity['username']
    user = userobj.getUser(entity['username'])
    print "user returned: ",  user
    if user!=None and user['password']==entity['password']:
        
        #Also set session id in the browser cookie
        session_id = sessionobj.start_session(user['username'] )
        response.set_cookie("session", session_id)
        data = {"result": True, "payload": user}
    else:
        data = {"result": False}
    
    return MongoEncoder().encode(data)

@route('/courseContentSelection', method='GET')
def courseContentSelection():
    print 'Bottle: you are in courseContentSelection'
    try:
        cursor = courseobj.getAll()
        entity = [d for d in cursor]
        print entity
    except:
        traceback.print_exc()
        abort(404, 'courses cannot be retrieved')    
        
    if not entity:
        abort(404, 'No course found')       
        
    return  MongoEncoder().encode(entity)


@route('/Course', method='POST')
def add_course():
    print 'You are in add_course service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for adding courses')
        
    entity = json.loads(data)
    
    email = entity['instructor'][0]['email']
    try:
        return {"success" : True, "id": str(courseobj.add(email, entity))}
    except:
        abort(400, 'Course not added')
        return {"success" : False}


@route('/course/enroll', method='PUT')
def enroll_course():
    print 'You are in enroll course service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for adding courses')
    entity = json.loads(data)
    try:
        courseobj.enroll(entity['email'], entity['courseid'])
    except:
        traceback.print_exc()
        abort(400, 'Course cannot be enrolled')    
        
@route('/course/drop', method='PUT')
def drop_course():
    print 'You are in drop course service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for droping courses')
    entity = json.loads(data)
    try:
        courseobj.drop(entity['email'], entity['courseid'])
    except:
        traceback.print_exc()
        abort(400, 'Course cannot be dropped')        

class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)     
     
@route('/course/:id', method='GET')
def get_course(id):
    print 'You are in get course service'
    
    try:
        entity = courseobj.get(id)
    except:
        traceback.print_exc()
        abort(404, 'Course cannot be retrieved')    
        
    if not entity:
        abort(404, 'No course with id %s' % id)       
        
    return MongoEncoder().encode(entity)

@route('/course/list', method='GET')
def getAll_course():
    print 'you are in getAll_course'
    try:
        cursor = courseobj.getAll()
        entity = [d for d in cursor]
        print entity
    except:
        traceback.print_exc()
        abort(404, 'courses cannot be retrieved')    
        
    if not entity:
        abort(404, 'No course found')       
        
    return  MongoEncoder().encode(entity)




@route('/course/:id', method='PUT')
def update_course(id):
    print 'You are in update course service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for updating courses')
    entity = json.loads(data)
    
    try:
        courseobj.update(id, entity)
    except:
        traceback.print_exc()
        abort(400, 'Course cannot be updated')    
        
    return "Course updated"

@route('/course/:id', method='DELETE')
def remove_course(id):
    print 'You are in delete course service'
    entity = courseobj.get(id)
        
    if not entity:
        abort(404, 'No course with id %s' % id)    
    try:
        courseobj.remove(id)
    except:
        traceback.print_exc()
        abort(400, 'course cannot be removed')
    
    return "Course deleted"



@route('/user', method='POST')
def add_user():
    print 'You are in add_user service'
    data = request.body.read()
    if not data:
     abort(400, 'No data received for adding courses')    
    entity = json.loads(data)
    
    if not entity.has_key('email'):
        abort(400, 'No email specified')
    try:
        userobj.addUser(entity)
    except:
        traceback.print_exc()
        abort(400, 'User not added')
    return 'user added'

@route('/user/:email', method='GET')
def get_user(email):
    print 'You are in get user service'
    print email
    try:
        entity = userobj.getUser(email)
        
    except:
        traceback.print_exc()
        abort(404, 'User cannot be retrieved')    
        
    if not entity:
        abort(404, 'No user with email %s' % email)       
        
    return MongoEncoder().encode(entity)

@route('/user/list', method='GET')
def getAll_user():
    print 'you are in getAll_user'
    try:
        cursor = userobj.getAll()
        entity = [d for d in cursor]
        print entity
    except:
        traceback.print_exc()
        abort(404, 'Users cannot be retrieved')    
        
    if not entity:
        abort(404, 'No User found')       
        
    return MongoEncoder().encode(entity)

@route('/user/:email', method='PUT')
def update_user(email):
    print 'You are in update user service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for updating users')
    entity = json.loads(data)
    
    try:
        userobj.updateUser(email, entity)
    except: 
        traceback.print_exc()
        abort(400, 'Cannot update User')    
        
    return "User updated"

@route('/user/course', method='PUT')
def update_UserCourse():
    print 'You are in update user course service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for updating user course')
    entity = json.loads(data)
    
    try:
        userobj.updateUserOwnCourse(entity['email'], entity['courseid'])
    except: 
        traceback.print_exc()
        abort(400, 'Cannot update User course')    
        
    return "User updated"


@route('/user/:email', method='DELETE')
def remove_user(email):
    print 'You are in delete user service'
    entity = userobj.getUser(email)
        
    if not entity:
        abort(404, 'No user with id %s' % email)    
    try:
        userobj.removeUser(email)
    except: 
        traceback.print_exc()
        abort(400, 'User cannot be removed')
    
    return "User deleted"


