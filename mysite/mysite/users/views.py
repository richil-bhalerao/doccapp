from django.contrib.auth import authenticate,login
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import moocsList,ipaddress
import json

def index(request):
   # val=request.GET['va']
    #print val
    uname=request.session['uid']
    return render_to_response('Home.html', {'userId': uname})

def login_view(request):

    state = "Please login below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                status=True
            else:
                state = "Your account is not active, please contact the site admin."
                status=True
        else:
            state = "Your username and/or password were incorrect." 
            status=True          
        if(status):
            request.session['uid']=username
            return render_to_response('Home.html',{'state':state, 'username': username},context_instance=RequestContext(request))
        else:
            return render_to_response('auth.html',{'state':state, 'username': username},context_instance=RequestContext(request))
    else:
        return render_to_response('auth.html',{'state':state, 'username': username},context_instance=RequestContext(request))
        
        
def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render_to_response('Logout.html',context_instance=RequestContext(request))

def mooclist(request):
    list =[]
    list= moocsList.objects.values()
    print "Hello"
    for val in list:
        print val
        success=True
    uname=request.session['uid']
    return render_to_response('moocList.html', {'userId': uname, 'success': success, 'list': list})

def exthome(request, path):
    # val=request.GET['va']
    #print val
    add=ipaddress(ip=path)
    add.save()
    val=[]
    val=ipaddress.objects.values()
    for v in val:
        print v
    uname=request.session['uid']
    return render_to_response('Home2.html', {'userId': uname, 'path': path})