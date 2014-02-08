"""
6, Apr 2013

Example bottle (python) RESTful web service.

This example provides a basic setup of a RESTful service

Notes
1. example should perform better content negotiation. A solution is
   to use minerender (https://github.com/martinblech/mimerender)
"""

import time
import sys
import socket

# bottle framework
from bottle import request, response, route, run, template, abort

# moo
from classroom import Room

#Ric Start
import traceback
from course import Course
from category import Category
from users import Users
from announcement import Announcement
from discussion import Discussion
from quiz import Quiz
from message import Message
import json
from inspect import trace
from bson.objectid import ObjectId
from json import JSONEncoder
#Ric End

# virtual classroom implementation
room = None
#Ric Start
courseobj = None
categoryobj = None
userobj = None
announcementobj = None
discussionobj = None
quizobj = None
messageobj = None
#Ric End

def setup(base,conf_fn):
   print '\n**** service initialization ****\n'
   global room, courseobj, categoryobj, userobj, announcementobj, discussionobj, quizobj, messageobj  
   room = Room(base,conf_fn)
   courseobj = Course()
   categoryobj = Category()
   userobj = Users()
   announcementobj = Announcement()
   discussionobj = Discussion()
   quizobj = Quiz()
   messageobj = Message()

#################################Ric Start#######################################################
@route('/course', method='POST')
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

#################################################################################################

@route('/category', method='POST')
def add_category():
    print 'You are in add_category service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for adding categories')
    entity = json.loads(data)
    
    try:
        return {"success" : True, "id": str(categoryobj.add(entity))}
    except:
        traceback.print_exc()
        abort(400, 'category cannot be added')
        return {"success" : False}    
     
@route('/category/:id', method='GET')
def get_category(id):
    print 'You are in get course service'
    try:
        entity = categoryobj.get(id)
    except:
        traceback.print_exc()
        abort(404, 'category cannot be retrieved')    
        
    if not entity:
        abort(404, 'No category with id %s' % id)       
        
    return MongoEncoder().encode(entity)

@route('/category/list', method='GET')
def getAll_category():
    print 'you are in getAll_categories'
    try:
        cursor = categoryobj.getAll()
        entity = [d for d in cursor]
        print entity
    except:
        traceback.print_exc()
        abort(404, 'categories cannot be retrieved')    
        
    if not entity:
        abort(404, 'No category found')       
        
    return MongoEncoder().encode(entity)

@route('/category/:id', method='PUT')
def update_category(id):
    print 'You are in update category service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for updating categories')
    entity = json.loads(data)
    
    try:
        categoryobj.update(id, entity)
    except:
        traceback.print_exc()
        abort(400, 'Category cannot be updated')    
        
    return "category updated"

@route('/category/:id', method='DELETE')
def remove_category(id):
    print 'You are in delete category service'
    entity = categoryobj.get(id)
        
    if not entity:
        abort(404, 'No category with id %s' % id)    
    try:
        categoryobj.remove(id)
    except:
        traceback.print_exc() 
        abort(400, 'Category cannot be removed')
    
    return "category deleted"

#################################################################################################

@route('/announcement', method='POST')
def add_announcement():
    print 'You are in add_announcement service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for adding announcements')
    entity = json.loads(data)
    
    try:
        return {"success" : True, "id": str(announcementobj.add(entity))}
    except:
        traceback.print_exc()
        abort(400, 'announcement cannot be added')
        return {"success" : False}    
     
@route('/announcement/:id', method='GET')
def get_announcement(id):
    print 'You are in get announcement service'
    try:
        entity = announcementobj.get(id)
    except:
        traceback.print_exc()
        abort(404, 'announcement cannot be retrieved')    
        
    if not entity:
        abort(404, 'No announcement with id %s' % id)       
        
    return MongoEncoder().encode(entity)

@route('/announcement/list', method='GET')
def getAll_announcement():
    print 'you are in getAll_announcement'
    try:
        cursor = announcementobj.getAll()
        entity = [d for d in cursor]
        print entity
    except:
        traceback.print_exc()
        abort(404, 'announcements cannot be retrieved')    
        
    if not entity:
        abort(404, 'No announcement found')       
        
    return MongoEncoder().encode(entity)

@route('/announcement/:id', method='PUT')
def update_announcement(id):
    print 'You are in update announcement service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for updating categories')
    entity = json.loads(data)
    
    try:
        announcementobj.update(id, entity)
    except:
        traceback.print_exc()
        abort(400, 'announcement cannot be updated')    
        
    return "announcement updated"

@route('/announcement/:id', method='DELETE')
def remove_announcement(id):
    print 'You are in delete announcement service'
    entity = announcementobj.get(id)
        
    if not entity:
        abort(404, 'No announcement with id %s' % id)    
    try:
        announcementobj.remove(id)
    except:
        traceback.print_exc() 
        abort(400, 'announcement cannot be removed')
    
    return "announcement deleted"

#################################################################################################

@route('/discussion', method='POST')
def add_discussion():
    print 'You are in add_discussion service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for adding discussions')
    entity = json.loads(data)
    
    try:
        return {"success" : True, "id": str(discussionobj.add(entity))}
    except:
        traceback.print_exc()
        abort(400, 'discussion cannot be added')
        return {"success" : False}    
     
@route('/discussion/:id', method='GET')
def get_discussion(id):
    print 'You are in get_discussion service'
    try:
        entity = discussionobj.get(id)
    except:
        traceback.print_exc()
        abort(404, 'discussion cannot be retrieved')    
        
    if not entity:
        abort(404, 'No discussion with id %s' % id)       
        
    return MongoEncoder().encode(entity)

@route('/discussion/list', method='GET')
def getAll_discussion():
    print 'you are in getAll_discussion'
    try:
        cursor = discussionobj.getAll()
        entity = [d for d in cursor]
        print entity
    except:
        traceback.print_exc()
        abort(404, 'discussions cannot be retrieved')    
        
    if not entity:
        abort(404, 'No discussion found')       
        
    return MongoEncoder().encode(entity)

@route('/discussion/:id', method='PUT')
def update_discussion(id):
    print 'You are in update discussion service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for updating discussions')
    entity = json.loads(data)
    
    try:
        discussionobj.update(id, entity)
    except:
        traceback.print_exc()
        abort(400, 'discussion cannot be updated')    
        
    return "discussion updated"

@route('/discussion/:id', method='DELETE')
def remove_discussion(id):
    print 'You are in delete discussion service'
    entity = discussionobj.get(id)
        
    if not entity:
        abort(404, 'No discussion with id %s' % id)    
    try:
        discussionobj.remove(id)
    except:
        traceback.print_exc() 
        abort(400, 'discussion cannot be removed')
    
    return "discussion deleted"

#################################################################################################

@route('/quiz', method='POST')
def add_quiz():
    print 'You are in add_quiz service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for adding quiz')
    entity = json.loads(data)
    
    try:
        return {"success" : True, "id": str(quizobj.add(entity))}
    except:
        traceback.print_exc()
        abort(400, 'quiz cannot be added')
        return {"success" : False}    
     
@route('/quiz/:id', method='GET')
def get_quiz(id):
    print 'You are in get quiz service'
    try:
        entity = quizobj.get(id)
    except:
        traceback.print_exc()
        abort(404, 'quiz cannot be retrieved')    
        
    if not entity:
        abort(404, 'No quiz with id %s' % id)       
        
    return MongoEncoder().encode(entity)

@route('/quiz/list', method='GET')
def getAll_quiz():
    print 'you are in getAll_quiz'
    try:
        cursor = quizobj.getAll()
        entity = [d for d in cursor]
        print entity
    except:
        traceback.print_exc()
        abort(404, 'quiz cannot be retrieved')    
        
    if not entity:
        abort(404, 'No quiz found')       
        
    return MongoEncoder().encode(entity)

@route('/quiz/:id', method='PUT')
def update_quiz(id):
    print 'You are in update quiz service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for updating quiz')
    entity = json.loads(data)
    
    try:
        quizobj.update(id, entity)
    except:
        traceback.print_exc()
        abort(400, 'quiz cannot be updated')    
        
    return "quiz updated"

@route('/quiz/:id', method='DELETE')
def remove_quiz(id):
    print 'You are in delete quiz service'
    entity = quizobj.get(id)
        
    if not entity:
        abort(404, 'No quiz with id %s' % id)    
    try:
        quizobj.remove(id)
    except:
        traceback.print_exc() 
        abort(400, 'quiz cannot be removed')
    
    return "quiz deleted"

#################################################################################################

@route('/message', method='POST')
def add_message():
    print 'You are in add_message service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for adding messages')
    entity = json.loads(data)
    
    try:
        return {"success" : True, "id": str(messageobj.add(entity))}
    except:
        traceback.print_exc()
        abort(400, 'message cannot be added')
        return {"success" : False}    
     
@route('/message/:id', method='GET')
def get_message(id):
    print 'You are in get message service'
    try:
        entity = messageobj.get(id)
    except:
        traceback.print_exc()
        abort(404, 'message cannot be retrieved')    
        
    if not entity:
        abort(404, 'No message with id %s' % id)       
        
    return MongoEncoder().encode(entity)

@route('/message/list', method='GET')
def getAll_message():
    print 'you are in getAll_message'
    try:
        cursor = messageobj.getAll()
        entity = [d for d in cursor]
        print entity
    except:
        traceback.print_exc()
        abort(404, 'messages cannot be retrieved')    
        
    if not entity:
        abort(404, 'No message found')       
        
    return MongoEncoder().encode(entity)

@route('/message/:id', method='PUT')
def update_message(id):
    print 'You are in update message service'
    data = request.body.read()
    if not data:
        abort(400, 'No data received for updating messages')
    entity = json.loads(data)
    
    try:
        messageobj.update(id, entity)
    except:
        traceback.print_exc()
        abort(400, 'message cannot be updated')    
        
    return "message updated"

@route('/message/:id', method='DELETE')
def remove_message(id):
    print 'You are in delete message service'
    entity = messageobj.get(id)
        
    if not entity:
        abort(404, 'No message with id %s' % id)    
    try:
        messageobj.remove(id)
    except:
        traceback.print_exc() 
        abort(400, 'message cannot be removed')
    
    return "message deleted"

#################################Ric End##########################################################



#################################Suma Start#######################################################
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


#################################Suma End##########################################################

# setup the configuration for our service
@route('/')
def root():
   print "--> root"
   return 'welcome'

#
#
@route('/moo/ping', method='GET')
def ping():
   return 'ping %s - %s' % (socket.gethostname(),time.ctime())

#
# Development only: echo the configuration of the virtual classroom.
#
# Testing using curl:
# curl -i -H "Accept: application/json" http://localhost:8080/moo/conf
#
# WARN: This method should be disabled or password protected - dev only!
#
@route('/moo/conf', method='GET')
def conf():
   fmt = __format(request)
   response.content_type = __response_format(fmt)
   return room.dump_conf(fmt)

#
# example of a RESTful method. This example is very basic, it does not 
# support much in the way of content negotiation.
#
@route('/moo/echo/:msg')
def echo(msg):
   fmt = __format(request)
   response.content_type = __response_format(fmt)
   if fmt == Room.html:
      return '<h1>%s</h1>' % msg
   elif fmt == Room.json:
      rsp = {}
      rsp["msg"] = msg
      return json.dumps(all)
   else:
      return msg


#
# example of a RESTful query
#
@route('/moo/data/:name', method='GET')
def find(name):
   print '---> moo.find:',name
   return room.find(name)

#
# example adding data using forms
#
@route('/moo/data', method='POST')
def add():
   print '---> moo.add'

   # example list form values
   for k,v in request.forms.allitems():
      print "form:",k,"=",v

   name = request.forms.get('name')
   value = request.forms.get('value')
   return room.add(name,value)

#
# Determine the format to return data (does not support images)
#
# TODO method for Accept-Charset, Accept-Language, Accept-Encoding, 
# Accept-Datetime, etc should also exist
#
def __format(request):
   #for key in sorted(request.headers.iterkeys()):
   #   print "%s=%s" % (key, request.headers[key])

   types = request.headers.get("Accept",'')
   subtypes = types.split(",")
   for st in subtypes:
      sst = st.split(';')
      if sst[0] == "text/html":
         return Room.html
      elif sst[0] == "text/plain":
         return Room.text
      elif sst[0] == "application/json":
         return Room.json
      elif sst[0] == "*/*":
         return Room.json

      # TODO
      # xml: application/xhtml+xml, application/xml
      # image types: image/jpeg, etc

   # defalult
   return Room.html

#
# The content type on the reply
#
def __response_format(reqfmt):
      if reqfmt == Room.html:
         return "text/html"
      elif reqfmt == Room.text:
         return "text/plain"
      elif reqfmt == Room.json:
         return "application/json"
      else:
         return "*/*"
         
      # TODO
      # xml: application/xhtml+xml, application/xml
      # image types: image/jpeg, etc
