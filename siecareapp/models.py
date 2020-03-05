from django.db import models

# Create your models here.

import os
from django.urls import reverse
from django.db.models import IntegerField, Model
from django_mysql.models import SetCharField
from django.contrib import admin
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail,mail_admins
from django.contrib.auth.models import User, Permission, Group
from django.db.models import Max
from django.db.models import Q
from django.db.models import Count
from django_mysql.models import ListCharField,ListTextField
from django.db.models import CharField, Model,TextField
import MySQLdb
from django.shortcuts import render

class Daycare(models.Model):
    name =models.CharField(max_length=255,default= 'NULL')
    location =models.CharField(max_length=255,default='NULL')
    segment=models.CharField(max_length=255,default='NULL')

    def __str__(self):
        return self.name

class Policies(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
