from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'email', 'contact_number', 'restaurant_name', 'issue_description', 'raised_to', 'photo']
