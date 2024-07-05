from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-contorol','placeholder':'Full Name'}),required=True)
    shipping_email = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-contorol','placeholder':'Email Address'}),required=True)
    shipping_address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-contorol','placeholder':'Address1'}),required=True)
    shipping_address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-contorol','placeholder':'Address2'}),required=False)
    shipping_state = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-contorol','placeholder':'STATE'}),required=False)
    shipping_city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-contorol','placeholder':'CITY'}),required=True)
    shipping_zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-contorol','placeholder':'ZIPCODE'}),required=False)
    shipping_country = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-contorol','placeholder':'COUNTRY'}),required=True)


    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name','shipping_email','shipping_address1','shipping_address2','shipping_state','shipping_city','shipping_zipcode','shipping_country']
        exclude = ['user',]