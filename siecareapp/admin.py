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
from django.shortcuts import render,render_to_response,redirect
from siecareapp.models import Daycare,Policies,Project_updates,TechnicalDocument,Female_count
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
  
  
  
    # readonly_fields = ["'description','document'"]
   
    def has_add_permission(self, request, obj=None):
       return False
    def has_delete_permission(self, request, obj=None):
       return False

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
            file_path = "C:\\Users\\z003tdhk\\clearing\\siecare\\documents\\understand_limitation.docx"
            
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
    change_form_template = "admin/TechnicalDoc/change_form.html"
    list_display = ('document_description','document',)
    list_filter = ('document_description','document',)
    list_per_page=10
    export_order = ('document_description',)
    actions = ["export_as_csv"]
    # # export_
    search_fields = ('document_description',)
   
    def has_add_permission(self, request, obj=None):
       return True
    def has_delete_permission(self, request, obj=None):
       return True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        
        return super(TechnicalDocumentAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
   
    def response_change(self, request, obj):
        
        if "_download_document" in request.POST:
            
            a=self.get_queryset(request).filter(document_description=obj).values_list('id')
            print(a)
            
            fs = FileSystemStorage()
            
            path = 'understand_limitation.docx'
            file_path = "C:\\Users\\z003tdhk\\clearing\\siecare\\documents\\understand_limitation.docx"
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
          
            print(file_path)
            
          
        return super().response_change(request, obj)
		

class ProjectResource(resources.ModelResource):

    class Meta:
        model = Project_updates
        skip_unchanged = True
        report_skipped = True

class ProjectUpdateAdmin(admin.ModelAdmin,CSSAdminMixin, ExportCsvMixin):
    change_form_template = "admin/Policies/change_form.html"
    # document = models.FileField(upload_to='documents/')
    list_display = ('project_name','department','information')
    list_filter = ('project_name','department',)
    list_per_page=10
    # list_display = ('name','location',)
    # list_filter = ['location','segment',]
    export_order = ('name','location','segment',)
    actions = ["export_as_csv"]
    # # export_
    search_fields = ('project_name','department','information',)
  
  
  
    # readonly_fields = ["'description','document'"]
   
    def has_add_permission(self, request, obj=None):
       return True
    def has_delete_permission(self, request, obj=None):
       return True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = True
        
        return super(ProjectUpdateAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
   
    # def response_change(self, request, obj):
        
    #     if "_download_document" in request.POST:
            
    #         a=self.get_queryset(request).filter(department=obj).values_list('project_name')
    #         print(a)


            
    #         fs = FileSystemStorage()

    #         path = 'understand_limitation.docx'
    #         file_path = "C:\\Users\\z003tdhk\\clearing\\siecare\\documents\\understand_limitation.docx"
            
    #         if os.path.exists(file_path):
    #             with open(file_path, 'rb') as fh:
    #                 response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
    #                 response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    #                 return response
          
    #         print(file_path)
            
          
        # return super().response_change(request, obj)


class FemalecountResource(resources.ModelResource):
    
    class Meta:
        model = Female_count
     

class FemalecountAdmin(admin.ModelAdmin,CSSAdminMixin, ExportCsvMixin):
    change_form_template = "admin/Release/change_form.html"
    resource_class = FemalecountResource
    list_per_page=10
    list_display = ('females',)
    list_filter = ['females',]
    # actions = ["export_as_csv"]
    # export_
    # search_fields = ('release',)
    def has_add_permission(self, request, obj=None):
       return True
    def has_delete_permission(self, request, obj=None):
        return True
    # def get_queryset(self, request):
    #     rel=[]
    #     ans=()
    #     database = MySQLdb.connect (host="localhost", user = "root", passwd = "", db = "siecare")

        
    #     cursor = database.cursor()
    #     try:
    #         query= "SELECT DISTINCT release_version FROM `new_partlist`"
    #         query2="SELECT 'RELEASE' FROM `new_release`"
    #         cursor.execute(query)
    #         ans=cursor.fetchall()
    #         cursor.execute(query2)
    #         ans1=cursor.fetchall()
    #         for i in ans:
    #             entry=Release.objects.filter(release=i[0]).count()
              
    #             if entry<1:
    #                 create_record=Release(release=i[0])
    #                 create_record.save()
    #     except :
    #         pass
        

        
    #     cursor.close()

        
    #     database.commit()

      
    #     database.close()

    #     print("")
    #     print("All Done! Bye, for now.")
    #     print("")
    #     qs= Release.objects.filter(~Q(release=""))
    #     return qs    
  
    #     print("All Done! Bye, for now.")
        # print("")
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        # name_eccn=['total','Going for Maternity']
        # dic={"name":name_eccn[val],"y":float(a)}
        responses_pie=[{'name': 'Total', 'y': 32.0},{'name':'Maternity','y': 10}]
  
        # create_record=list(Release.objects.filter(id=object_id))
        # rel_info=create_record[0]
        # j1=[]
        # h1=[]
        # k1=[]
        # a1=[]
        # c=0
        # count=0
        # a=0
       
        # # new1 = Applicationsoftware.objects.all()
        

        # ans1=[]
        # ans=[]
        # name_eccn=[]
        # responses_pie=[]
        # dic={}
        # new = Systemsoftware.objects.all()
       
       
       
        # qs=new.filter(release_in_which_component_used__contains=rel_info)
   

        # database = MySQLdb.connect (host="localhost", user = "root", passwd = "", db = "oss1")

        
        # cursor = database.cursor()
        # query= "SELECT DISTINCT eccn FROM `new_systemsoftware`"
        # # query1= "SELECT DISTINCT eccn FROM `new_applicationsoftware`"
        
        # cursor.execute(query)
        # ans=list(cursor.fetchall())
        # # cursor.execute(query1)
        # # ans1=list(cursor.fetchall())
      
        
        # cursor.close()

        
        # database.commit()

      
        # database.close()
        # # ans=Union(ans, ans1)
        # for val in range(0,len(ans)):

        #       if ans[val][0] is None:
        #         continue
        #       if ans[val][0] == "":
        #         continue
        #       name_eccn.append(ans[val][0])
        # # print(ans)
        # # print(ans1)
        # # print("union")
        # print(name_eccn)
        # name_eccn_flag=0
               
                
  

        # for val in range(0,len(name_eccn)):
                
        #         a= qs.filter(eccn=name_eccn[val]).count()
        #         # b=new1.filter(eccn=name_eccn[val]).count()
        #         # a=a+b
        #         print(name_eccn[val])
        #         print(len(name_eccn[val]))

                
        #         if len(name_eccn[val]) == 1 and name_eccn[val]!="N":
                    
        #             count=a
        #             print(count)
        #             a=0
                    
        #         if name_eccn[val]=="None":
        #             print("d=None")
        #             c=a
        #             print(c)
        #             a=0
        #         if name_eccn[val]=="#N/A" :
        #             name_eccn_flag=name_eccn_flag+1
        #             print("d=1")
        #             a=a+count+c
                
        #         if (c>0 or count>0):
        #             if "#N/A" not in name_eccn:
        #                 print("d=0")
        #                 name_eccn[val]="#N/A"
        #                 a=count+c
                   
        #         if a>0 and name_eccn[val]!="None":
        #             print(name_eccn[val])
        #             print(float(a))
        #             dic={"name":name_eccn[val],"y":float(a)}
                
        #             responses_pie.append(dic)
        # print(responses_pie)
        return render(request,'admin/Release/change_form.html',{'responses_pie': responses_pie})
        pass
        # return {'responses_pie': responses_pie}
        # pass
        return super(FemalecountAdmin, self).changeform_view(request, object_id, extra_context=extra_context)



admin.site.register(Daycare,DaycareAdmin)
admin.site.register(Policies,PoliciesAdmin)
admin.site.register(Project_updates,ProjectUpdateAdmin)
admin.site.register(TechnicalDocument,TechnicalDocumentAdmin)
admin.site.register(Female_count,FemalecountAdmin)