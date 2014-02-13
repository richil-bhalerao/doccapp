from django.db import models

class moocsList(models.Model):
    team = models.CharField(max_length=30)
    path=models.CharField(max_length=100)
    
class ipaddress(models.Model):
    ip=models.CharField(max_length=30)
    
class registerUser(models.Model):
    username=models.TextField(max_length=20)
    email=models.EmailField(max_length=30)
    password=models.TextField(max_length=20)
    fname=models.TextField(max_length=30)
    lname=models.TextField(max_length=30)
    
    
