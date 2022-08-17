from django import forms
from .models import Message

class CreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['key', 'message']

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
