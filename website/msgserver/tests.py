from django.test import TestCase
from .models import Message
import string, random, json

KEYLENGTH = 8
MESSAGE_MAX_LENGTH = 160

def getRandKey(length):
    num = string.digits
    alpha = string.ascii_lowercase
    alphaNumKey = ''.join(random.choice(num + alpha) for i in range(length))
    return alphaNumKey

def getRandMsg(length):
    alpha = string.ascii_lowercase
    randomMessage = ''.join(random.choice(alpha) for i in range(length))
    return randomMessage

# Create your tests here.

class MessageTestCreate(TestCase):
    def test_create_and_retrieve(self):
        randKey = getRandKey(KEYLENGTH)
        randMessage = getRandMsg(MESSAGE_MAX_LENGTH)
        self.client.post("/msgserver/create/", {'key':randKey, 'message':randMessage})
        responseMessage = Message.objects.get(key=randKey)
        self.assertEqual(responseMessage.key, randKey)
        self.assertEqual(responseMessage.message, randMessage)

    def test_no_duplicates(self):
        randKey = getRandKey(KEYLENGTH)
        randMessage = getRandMsg(MESSAGE_MAX_LENGTH)
        self.client.post("/msgserver/create/", {'key':randKey, 'message':randMessage})
        responseMessage = Message.objects.get(key=randKey)
        self.client.post("/msgserver/create/", {'key':randKey, 'message':randMessage + '1'})
        responseMessageTwo = Message.objects.get(key=randKey)
        p = Message.objects.all()
        if len(p) != 1:
            print(response, p)
            self.fail()
        self.assertEqual(responseMessage.key, randKey)
        self.assertEqual(responseMessage.message, randMessage)

    def test_key_message_constraints(self):
        #this test needs to be reworked. 
        randKey = getRandKey(KEYLENGTH)
        randMessage = getRandMsg(MESSAGE_MAX_LENGTH + 1) #outside of the message length constraint
        send = self.client.post("/msgserver/create/", {'key':randKey, 'message':randMessage})
        #enter a try..except here - when try fails, the message was not created, as it should be.
        #self.assertIn(b'The text on the page!', send.content)
        try:
            responseMessage = Message.objects.get(key=randKey)
            self.fail()
        except:
            pass

    def test_message_updates(self):
        randKey = getRandKey(KEYLENGTH)
        testKey = getRandKey(10) #arbitrary key length that can be tested against when appending to a message string
        randMessage = getRandMsg(MESSAGE_MAX_LENGTH - 10) #ten less than max - add a final character to the message
        self.client.post("/msgserver/create/", {'key':randKey, 'message':randMessage})
        self.client.post("/msgserver/update/" + randKey + "/", {'message':(randMessage + testKey)}) #append an X
        updatedMsg = Message.objects.get(key=randKey)
        self.assertEqual(updatedMsg.message, randMessage + testKey) #see if the updated message has an X

    def test_retrieve_as_json(self):
        randKey = getRandKey(KEYLENGTH)
        randMessage = getRandMsg(MESSAGE_MAX_LENGTH)
        self.client.post("/msgserver/create/", {'key':randKey, 'message':randMessage})
        #messagedatastring = "\"pk\": \"{}\", \"fields\": {\"message\": \"{}\"}".format(randKey, randMessage)
        #self.assertJSONEqual(response.content, messagedatastring)
        response = self.client.get("/msgserver/")
        try:
            if randKey and randMessage in str(response.content):
                pass
            else:
                self.fail()
        except:
            self.fail()
