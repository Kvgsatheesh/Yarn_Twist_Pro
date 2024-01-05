from django import forms
from django.forms import ModelForm
from .models import *


class dateform(forms.Form):
   From= forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
   To=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
class Addcompanyform(forms.ModelForm):
    
    class Meta:
        model=Company
        fields="__all__"

class addstaffform(forms.ModelForm):
    class Meta:
        model=Staffprofile
        fields="__all__"

class addcountform(forms.ModelForm):
    class Meta:
        model=Count
        fields="__all__"

class addtpform(forms.ModelForm):
    class Meta:
        model=Tp
        fields="__all__"

class Addcolourform(forms.ModelForm):

    class Meta:
        model=Colour
        fields='__all__'
    
class addinventryform(forms.ModelForm):
    
    class Meta:
        model=Stocks
        fields=['Company','Colour','Count','Tp','Inward',]

class outwardform(ModelForm):
    class Meta:
        model=Stocks
        fields=['Company','Colour','Count','Tp','Outward',]

class updateform(ModelForm):
    class Meta:
        model=Stocks
        fields=['Company','Colour','Count','Tp']

class paymentform(ModelForm):
    class Meta:

        model=Stocks
        fields=['Company','Colour','Count','Tp','Bag','Amount']


class returnform(ModelForm):
    class Meta:
        model=Stocks
        fields=['Company','Colour','Count','Tp','Inward',]

class addproductionform(forms.ModelForm):
    class Meta:
        model=Production
        fields=['Staff','Company','Colour','Count','Tp','Cheese_bag','Doubled_bag','Tfo_shift','Waste']

class addpriceform(forms.ModelForm):
    class Meta:
        model=Price
        fields='__all__'

class addexpenseform(forms.ModelForm):
    class Meta:
        model=Expense
        fields='__all__'


class addadvanceandbonusform(forms.ModelForm):
    class Meta:
        model=Others
        fields='__all__'
    
class addotherincomeform(forms.ModelForm):
    class Meta:
        model=Otherincome
        fields='__all__'
