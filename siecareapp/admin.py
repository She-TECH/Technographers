from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse,HttpResponseNotFound
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
from siecareapp.models import Daycare,Policies,TechnicalDocument
from django.conf import settings
from django.core.exceptions import ValidationError
import requests
from import_export import resources
import csv
from django.core.files.storage import get_storage_class, FileSystemStorage

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

class PoliciesResource(resources.ModelResource):

    class Meta:
        model = Policies
        skip_unchanged = True
        report_skipped = True

class PoliciesAdmin(admin.ModelAdmin,CSSAdminMixin, ExportCsvMixin):
    change_form_template = "admin/Policies/change_form.html"
    # document = models.FileField(upload_to='documents/')
    list_display = ('description','document',)
    list_filter = ('description','document',)
    list_per_page=10
    actions = ["export_as_csv"]
    # # export_
    search_fields = ('description')
  
    def has_add_permission(self, request, obj=None):
       return True
    def has_delete_permission(self, request, obj=None):
       return True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        
        return super(PoliciesAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
   
    def response_change(self, request, obj):
        
        if "_download_document" in request.POST:
            
            a=self.get_queryset(request).filter(description=obj).values_list('id')
            print(a)
            
            fs = FileSystemStorage()
            
            path = 'understand_limitation.docx'
            file_path = "C:\\Users\\Karishma Mahajan\\Desktop\\Technographers\\documents\\understand_limitation.docx"
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
          
            print(file_path)
            
          
        return super().response_change(request, obj)

class TechnicalDocumentResource(resources.ModelResource):

    class Meta:
        model = TechnicalDocument
        skip_unchanged = True
        report_skipped = True

class TechnicalDocumentAdmin(admin.ModelAdmin,CSSAdminMixin, ExportCsvMixin):
    technical_document_template = "admin/TechnicalDocument/technical_document.html"
    list_display = ('document_description','document',)
    list_filter = ('document_description','document',)
    list_per_page=10
    export_order = ('document_description')
    actions = ["export_as_csv"]
    # # export_
    search_fields = ('document_description')
   
    def has_add_permission(self, request, obj=None):
       return True
    def has_delete_permission(self, request, obj=None):
       return True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        
        return super(TechnicalDocumentAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
   
    def response_change(self, request, obj):
        
        if "_download_technical_doc" in request.POST:
            
            a=self.get_queryset(request).filter(description=obj).values_list('id')
            print(a)
            
            fs = FileSystemStorage()
            
            path = 'understand_limitation.docx'
            file_path = "C:\\Users\\Karishma Mahajan\\Desktop\\Technographers\\documents\\understand_limitation.docx"
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
          
            print(file_path)
            
          
        return super().response_change(request, obj)


admin.site.register(Daycare,DaycareAdmin)
admin.site.register(Policies,PoliciesAdmin)
admin.site.register(TechnicalDocument,TechnicalDocumentAdmin)