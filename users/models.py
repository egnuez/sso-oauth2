from django.db import models
from django.utils.text import slugify

# Create your models here.

class Apps(models.Model):
    name = models.CharField(max_length=64)
    secret = models.CharField(max_length=64)

class Resources(models.Model):
    name = models.CharField(max_length=64)
    app = models.ManyToManyField(Apps)

class Users(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    app = models.ManyToManyField(Apps)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(Users, self).save(*args, **kwargs)

    @property
    def str_apps(self):
        return [ app.name for app in self.app.all() ]
