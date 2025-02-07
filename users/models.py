from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"  # set email as the login field
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    def __str__(self):
        return self.username
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=180)
    date = models.DateField()
    time = models.TimeField()
    price = models.FloatField()
    image =  models.CharField(max_length=240) 
    no_of_tickets = models.PositiveIntegerField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Hotels(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.CharField(max_length=240)
    rating = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
 
    def __str__(self):
        return self.nameield()
    
class Movies(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    rating = models.IntegerField() 
    price = models.FloatField() 
    duration = models.PositiveIntegerField()
    date = models.DateField()
    poster = models.CharField(max_length=240)
    no_of_tickets = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title