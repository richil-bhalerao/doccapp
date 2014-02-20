from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    (r'^signIn/$','mysite.users.views.login_view'),
    (r'^index/$','mysite.users.views.index'),
    (r'^logout/$','mysite.users.views.logout'),
    (r'^course/$','mysite.users.views.addcourse'),
     (r'^register/$','mysite.users.views.createUser'),
     (r'^courseContentSelection/$','mysite.users.views.courseContentSelection'),
    # Uncomment the admin/doc line below to e(r'^register/$','mysite.users.views.createUser'),nable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
    
    url(r'^exthome/([a-zA-Z0-9_:./]*)$', 'mysite.users.views.exthome', name='exthome'),
)
