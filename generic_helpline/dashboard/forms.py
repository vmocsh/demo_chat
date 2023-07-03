from django import forms
from django.forms import ModelForm
from registercall.models import Task
from management.models import HelpLine, HelperCategory, CategorySubcategory
from constants import *
from ivr.models import Language

# class CategoriesType:

    

    


class AddTask(forms.Form):
    name = forms.CharField(label="Your name", max_length=20)
    phone = forms.CharField(max_length=10)
    location = forms.CharField(label="Location", max_length=20)
    category = forms.ModelChoiceField(queryset=HelperCategory.objects.all())
    language = forms.ModelChoiceField(queryset=Language.objects.all())

