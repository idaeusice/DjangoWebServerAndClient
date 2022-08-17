from django.shortcuts import HttpResponse, render
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
from .models import Message
from .forms import CreateForm, UpdateForm
import json

KEYLENGTH = 8

def keyValid(key):
    if key.isalnum():
        return True
    else:
        return False

def messages(request, key):
    string = Message.objects.filter(key=key)
    if (len(key) == KEYLENGTH):
        return HttpResponse("%(key)s%(message)s" 
% {'key':str(string[0].key), 'message':str(string[0].message) })
    else:
        return HttpResponse('Key did not match')


#
#Handling for /msgserver/create/
#
def createMessage(request):
    form = CreateForm(request.POST)
    messages = Message.objects.all()
    context = {
        'form': form
    }

    if form.is_valid() and keyValid(form.cleaned_data['key']):
        submittedkey = form.cleaned_data['key']
        submittedmessage = form.cleaned_data['message']
        for message in messages:
            if submittedkey == message.key:
                #true when there is an existing match for the key, need to reassign key here somehow
                return render(request, "templates/msgserver/message_form.html", context)
        form.save()
        return HttpResponseRedirect('/msgserver/')
    else:
        return render(request, "templates/msgserver/message_form.html", context)

#PURPOSE:
#Handling for msgserver/update/
#
#
#
#
#
#
def updateMessage(request, key):
    key = key
    messages = Message.objects.all()
    thismessage = Message.objects.get(key=key)
    #first visit is get
    if request.method == 'GET':
        form = UpdateForm(initial={'key': key, 'message': thismessage.message})

    if request.method == 'POST':
        form = UpdateForm(request.POST)

    context = {
        'form': form
    }
    if form.is_valid() and keyValid(key):
        messages.filter(key=key).update(message=form.cleaned_data['message'])
        return HttpResponseRedirect('/msgserver/')
    return render(request, "templates/msgserver/message_form.html", context)

#PURPOSE:
#displays all messages and keys as key-value pairs in json format.
#
#PARAMETERS:
#the HttpRequest object created by django when reaching msgserver/
#
#RETURNS:
#an HttpResponse object that renders the message data in json format.
def showall(request):
    message = serializers.serialize('json', Message.objects.all().only('key', 'message'))
    jsonstring = json.dumps(message)
    return HttpResponse(jsonstring.replace("\\", ""),content_type='application/json')
