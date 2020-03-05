from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from django.db import models
from django.db.models import Max,Count,Q
from django.db.models.functions import Length
from itertools import islice, chain
from django import forms
from datetime import date
import xlwt
import sys
from django.db import IntegrityError
from import_export.admin import ImportExportActionModelAdmin
from import_export.fields import Field
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
import re
import datetime
import os
import numpy as np
import MySQLdb
from siecareapp.views import index
from django_mysql.models import ListF
from openpyxl import load_workbook
from django.shortcuts import render
from siecareapp.models import Daycare
from django.core.exceptions import ValidationError
import requests
from import_export import resources
import csv

class CSSAdminMixin(object):
    class Media:
        css = {
            'all': ('css/admin.css',),
        }

def export_as_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class DaycareResource(resources.ModelResource):
  
    class Meta:
        model = Daycare
        export_order = ('name','location','segment',)
        # export_order = ('sw_name','version','vendor_name','homepage','license_type','dev_contact','eccn','al','comment','license_clearing','major_version',)
        # exclude = ('id', 'partlist_name' )
class DaycareAdmin(ImportExportModelAdmin,ExportCsvMixin):
    resource_class = DaycareResource
    # change_list_template = "admin/new/Systemsoftware/change_list.html"
    list_per_page=10
    list_display = ('name','location',)
    list_filter = ['location','segment',]
    export_order = ('name','location','segment',)
    actions = ["export_as_csv"]
    # # export_
    search_fields = ('name','location','segment',)
    # def has_add_permission(self, request, obj=None):
    #    return True
    # def has_delete_permission(self, request, obj=None):
    #     return True
    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['show_save_and_continue'] = True
    #     return super(SystemsoftwareAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
   
    # def get_queryset(self, request):
       
    #     qs =Daycare.objects.all()

admin.site.register(Daycare,DaycareAdmin)