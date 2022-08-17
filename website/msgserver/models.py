from django.db import models
from django import forms
from django.core.exceptions import ValidationError

def validate_key(value):
    if len(value) != 8:
        raise ValidationError('Key must be 8 characters', code='key_size')

def validate_message(value):
    if len(str(value)) > 160 or len(value) < 1:
        raise ValidationError('Message must be between 1 and 160 characters', code='message_size')

# Create your models here.
class Message(models.Model):
    key = models.CharField(primary_key=True, max_length=8, validators=[validate_key])
    message = models.TextField(max_length=160)

    def __str__(self):
        return str(self.key) + ': ' + str(self.message)

class Create(models.Model):
    keyfield = forms.CharField(max_length=8, validators=[validate_key])
    messagefield = forms.CharField(widget=forms.Textarea, label='Message: ',
max_length=160, validators=[validate_message])

class Update(models.Model):
    keyfield = forms.CharField(label='Key: ', max_length=8, validators=[validate_key])
    messagefield = forms.CharField(widget=forms.Textarea, label='Message: ',
max_length=160, validators=[validate_message])
