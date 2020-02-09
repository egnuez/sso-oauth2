from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

class Apps(models.Model):
    name = models.CharField(max_length=64)