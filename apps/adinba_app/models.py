from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone
# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    primary_number = models.CharField(max_length = 255, blank = True, default = None)
    secondary_number = models.CharField(max_length = 255, blank = True, default = None)
    business_owner = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Business(models.Model):
    title = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 255)
    zip = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    primary_number = models.CharField(max_length = 255)
    secondary_number = models.CharField(max_length = 255, blank = True, default = None)
    business_email = models.CharField(max_length=  255)
    website = models.CharField(max_length = 255, blank = True, default = None)
    facebook = models.CharField(max_length = 255, blank = True, default = None)
    twitter = models.CharField(max_length = 255, blank = True, default = None)
    instagram = models.CharField(max_length = 255, blank = True, default = None)
    yelp = models.CharField(max_length = 255, blank = True, default = None)
    pending = models.BooleanField(default = True)
    user_id = models.ForeignKey(User, related_name = "owner")
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(default = timezone.now)

class Event(models.Model):
    title = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 255)
    zip = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    primary_number = models.CharField(max_length = 255)
    primary_contact = models.CharField(max_length = 255)
    contact_email = models.CharField(max_length = 255)
    starting_date = models.CharField(max_length = 255)
    ending_date = models.CharField(max_length = 255)
    pending = models.BooleanField(default = True)
    business_id = models.ForeignKey(Business, related_name = "event_host") 
    users = models.ManyToManyField(User, related_name = "attendee")
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(default = timezone.now)

class Special(models.Model):   
    title = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    category = models.CharField(max_length = 255)
    starting_date = models.CharField(max_length = 255)
    ending_date = models.CharField(max_length = 255)
    pending = models.BooleanField(default = True)
    business_id = models.ForeignKey(Business, related_name = "specials_host") 
    users = models.ManyToManyField(User, related_name = "claimee")
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(default = timezone.now)

class Message(models.Model):
    name = models.CharField(max_length = 255)
    message = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
