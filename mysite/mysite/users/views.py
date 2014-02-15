from django.contrib.auth import authenticate,login
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import moocsList,ipaddress,registerUser
import json, requests
from django.http import *

def index(request):
   # val=request.GET['va']
    #print val
    #uname=request.session['uid']
    return render_to_response('Home.html')

def login_view(request):

    state = "Please login below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username;
        print password;
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                status=True
                print "logged in"
            else:
                state = "Your account is not active, please contact the site admin."
                status=False
                print "incorrect login"
        else:
            state = "Your username and/or password were incorrect." 
            status=False          
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
      payload = {"username":username,"email":email,"fname":fname,"lname":lname}
      print payload
      status=requests.post(url='http://127.0.0.1:8080/register',data=json.dumps(payload), headers=headers)
      print status.status_code
      if(status.status_code==200):  
         print status  
         return render_to_response('Home.html',context_instance=RequestContext(request))
      else:
         status = 401 
         return HttpResponseRedirect('http://google.com')
         print status
   # Get all posts from DB
   return render_to_response('registration.html', {'user': payload},
                             context_instance=RequestContext(request))
        
def addCourse(request):
   if request.POST:
        form = CourseForm(request.POST)
        if form.is_valid():
            global success
            global userId
            category = request.POST.get('category')
            title = request.POST.get('title')
            section = request.POST.get('section')
            dept=request.POST.get('dept')
            term=request.POST.get('term')
            year=request.POST.get('year')
            instructorname=request.POST.get('instructorname')
            instructoremail=request.POST.get('instructoremail')
            days=request.POST.get('days')
            hours=request.POST.get('hours')
            description=request.POST.get('description')
            attachment=request.POST.get('attachment')
            version=request.POST.get('version')
            
            
            
            
            
            
            category = form.cleaned_data['category']
            title = form.cleaned_data['title']
            section= form.cleaned_data['section']
            dept=form.cleaned_data['dept']
            term=form.cleaned_data['term']
            year=form.cleaned_data['year']
            instructorname=form.cleaned_data['instructorname']
            instructoremail=form.cleaned_data['instructoremail']
            days=form.cleaned_data['days']
            hours=form.cleaned_data['hours']
            description=form.cleaned_data['description']
            attachment=form.cleaned_data['attachment']
            version=form.cleaned_data['version']
            
            print category
            print title
            print section
            userId=request.session['uid']
            success = True
            
            headers = {'content-type': 'application/json'}
            payload = {
            "category": str(category),
#            "id":"test1",
            "title": str(title),
            "section": str(section),
            "dept": str(dept),
            "term": str(term),
            "year": str(year),
            "instructor": [
            {
            "name": instructorname,
            "email": instructoremail
            }
            ],
            "days": [
            "Monday",
            "Wednesday",
            "Friday"
            ],
            "hours": [
            "8:00AM",
            "9:15:AM"
            ],
            "Description": description,
            "attachment": "",
            "version": version
            }
            
            jsonData=json.dumps(payload)
#             formData = {'category': category, 'title': title, 'section': section, 'dept':dept, 'term':term, 'year':year,'instructor:[{/'name/''}    
#             formDataInJson = json.dumps(formData)
            #print 'formDataInJson : ' , formDataInJson
            
            #Send the Add User Request and get the status 
            list= ipaddress.objects.values()
            for val in list:
                ipadd = val
           
            ipadd = ipadd['ip']
               
            print "current ipaddress is ", ipadd
            
            #url= "http://"+ipadd+"/course" 
            url="http://127.0.0.1:8080/course"
            print "URL : ",url
#           
           # status = urllib2.urlopen(url)
            course=requests.post(url,data=json.dumps(payload),headers=headers)
            print course
           # status = json.loads('{"success": true}')
            #print 'Status Json : ' , status  
            #status['success'] = False   
#             url= "http://localhost:8080/user/course"
#             cid=course['id']
#             
#             print "cid=",cid
#             payload={"email":userId, "courseid":cid}
#             requests.put(url,data=json.dumps(payload),headers=headers)
#         
#                return render_to_response('userAdd.html', {'userId': userId, 'form': form, 'success': success}) 
            return render_to_response('AddSuccess.html',{ 'userId': userId},context_instance=RequestContext(request))
            
   else:
           
            userId=request.session['uid']
            success = False
            form = CourseForm()
            return render_to_response('courseAdd.html', {'userId': userId, 'form': form},context_instance=RequestContext(request))
        
        