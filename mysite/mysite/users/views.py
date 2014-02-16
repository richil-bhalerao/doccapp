from django.contrib.auth import authenticate,login
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import moocsList,ipaddress,registerUser
import json, requests, base64
from django.http import *

def index(request):
   # val=request.GET['va']
    #print val
    #uname=request.session['uid']
    return render_to_response('Home.html', context_instance=RequestContext(request))

def login_view(request):

    state = "Please login below..."
    username = password = ''
    payload=''
    headers=''
    headers = {'content-type': 'application/json'}

    username = request.GET.get('username')
    password = request.GET.get('password')
    print username;
    print password;
    encryptedPassword = base64.b64encode(password)
    payload = {"username":username,"password":encryptedPassword}
    print payload
    status=requests.get(url='http://127.0.0.1:8080/signIn',data=json.dumps(payload), headers=headers)
    return render_to_response('auth.html',{'state':state, 'username': username},context_instance=RequestContext(request))

def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render_to_response('Logout.html',context_instance=RequestContext(request))


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
        
