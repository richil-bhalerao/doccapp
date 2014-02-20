from django.contrib.auth import authenticate,login
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import moocsList,ipaddress,registerUser
import json, requests, base64
from django.http import *
import urllib2, urllib

def index(request):
   # val=request.GET['va']
    #print val
    #uname=request.session['uid']
    return render_to_response('index.html', context_instance=RequestContext(request))

def login_view(request):

    state = "Please login below..."
    username = password = ''
    payload=''
    headers=''
    headers = {'content-type': 'application/json'}

    username = request.GET.get('username')
    password = request.GET.get('password')
    
    encryptedPassword = base64.b64encode(password)
    payload = {"username":username,"password":encryptedPassword}
    
    status=requests.put(url='http://127.0.0.1:8080/signIn', data=json.dumps(payload), headers=headers)
    jsonData = status.json()
    result = jsonData['result']
    if result==False:
        return render_to_response('loginfailed.html',{'state':"Username or password is invalid", 'username': username},context_instance=RequestContext(request))
    else:
        #request.session['session']
        return render_to_response('welcome.html',{'state':"User logged in successfully", 'user': jsonData['payload']},context_instance=RequestContext(request))

def logout(request):
    try:
        print 'hi'
        #del request.session['uid']
    except KeyError:
        pass
    return render_to_response('index.html',context_instance=RequestContext(request))


def createUser(request):
   print 'in create user'
   payload=''
   headers=''
   headers = {'content-type': 'application/json'}
   if request.method == 'POST':
      # save new post
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      fname = request.POST['fname']
      lname = request.POST['lname']
      encryptedpassword = base64.b64encode(password)
      payload = {"username":username, 'password':encryptedpassword,"email":email,"fname":fname,"lname":lname}
      print payload
      status=requests.post(url='http://127.0.0.1:8080/register',data=json.dumps(payload), headers=headers)
      print status.status_code
      if(status.status_code==200):  
         print status  
         return HttpResponseRedirect('http://127.0.0.1:8000/index')
      else:
         status = 401 
         return HttpResponseRedirect('http://google.com')
         print status
   # Get all posts from DB
   return render_to_response('Home.html', {'user': payload},
                             context_instaindexnce=RequestContext(request))
   
def courseContentSelection(request):
    print 'Django: In course content selection page'
    status = requests.get(url='http://127.0.0.1:8080/courseContentSelection')
    print status.json()
    data = status.json()
    return render_to_response('courseContentSelection.html', {'data':data}, context_instance=RequestContext(request))
        
