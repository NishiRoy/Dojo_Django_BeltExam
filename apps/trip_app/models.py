from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from datetime import date

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['fName']) < 3:
            errors["name"] = "Name has to be more than 5 characters"
        print len(postData['lName'])
        if len(postData['lName']) < 3:
            errors['desc'] = "Description has to be more than 10 characters"
        if len(postData['email']) >3:
            try:
                validate_email(postData['email'])
            except ValidationError as e:
                errors['email']="Wrong Email"
        # if (postData['date'] == None):
        #     errors['birthday'] = 'Please enter a birthday'
        if len(postData['password']) < 8:
            errors["name"] = "Password has to be more than 8 characters"
        if len(postData['cpassword']) < 8:
            errors['desc'] = "Password confirmation has to be more than 8 characters"
        if postData['password']!=postData['cpassword']:
            errors['password']="Password confirmation does not match Password"
        
        return errors

class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email_address=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return "<Object name{},lastname {},email{}>".format(self.first_name,self.last_name,self.email_address)

    objects=UserManager()

class Travel(models.Model):
    destination=models.CharField(max_length=255)
    start_date=models.DateTimeField(auto_now_add=False)
    end_date=models.DateTimeField(auto_now_add=False)
    plan=models.CharField(max_length=255,default=None)
    travellers=models.ManyToManyField(Users,related_name="destina")
    owner=models.ForeignKey(Users,related_name="creator")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "< Place{}, start_date {}, end_date{}>".format(self.destination,self.start_date,self.end_date)