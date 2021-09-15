from django.db import models
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"
        users_with_email = User.objects.filter(email = postData['email'])
        if len(users_with_email) >= 1:
            errors['duplicate'] = "Email already exists."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        return errors

class LocationManager(models.Manager):
    def location_validator(self, postData):
        errors = {}
        if postData['name'] == "":
            errors['name'] = "Location cannot be blank"
        if postData['address'] == "":
            errors['address'] = "Address cannot be blank"
        if postData['zip_code'] =="":
            errors['zip_code'] = "Zip Code cannot be blank"
        return errors

class ActivityManager(models.Manager):
    def activity_validator(self, postData):
        errors = {}
        if postData['name'] == "":
            errors['name'] = "Activity cannot be blank"

        if postData['activity_date'] =="":
            errors['activity_date'] = "Please enter a Activity Date and Time"
        elif datetime.strptime(postData['activity_date'], '%Y-%m-%dt%H:%M') < datetime.now():
            errors['activity_date'] = "Activity Date and Time should be in the future"

        return errors



class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=15)
    objects = LocationManager()
    



class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Activity (models.Model):
    name = models.CharField(max_length=50)
    activity_date = models.DateTimeField()
    desc = models.TextField(blank=True)
    activityType = models.CharField(max_length=10)
    location = models.ForeignKey(Location, blank=True, null=True,related_name="activities", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="activity", on_delete = models.CASCADE)
    attendee = models.ManyToManyField(User,blank=True, related_name="joined_activity")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ActivityManager()

        

