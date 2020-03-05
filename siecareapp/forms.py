from django import forms
from siecareapp.models import Policies

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Policies
        fields = ('description', 'document', )