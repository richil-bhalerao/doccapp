from django.db import models

class moocsList(models.Model):
    team = models.CharField(max_length=30)
    path=models.CharField(max_length=100)
    
class ipaddress(models.Model):
    ip=models.CharField(max_length=30)
