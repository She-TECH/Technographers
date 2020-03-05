from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from siecareapp.forms import DocumentForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        form.save()
        if form.is_valid():
            print("successful")
        #     form.save()
        #     return 1
        form.save()
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })