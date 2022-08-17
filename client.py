#!/usr/bin/env python3
import requests
import sys, random, string, json

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

def client(ip, port, key):
    nextkey = key
    while True:
        request = requests.get('http://' + ip + ':' + port + '/msgserver/get/' + nextkey + '/')
        data = request.content
        #if the returned contains no data - result is html from the page (opening tag):
        if data.decode('utf-8')[0:1:] == '<':
            break
        #if there IS data:
        else:
            body = data.decode('utf-8')[KEYLENGTH::]
            nextkey = body[0:KEYLENGTH:]
            print(body[KEYLENGTH::])

    client = requests.session()
    url = 'http://' + ip  +':' + port + '/msgserver/create/'
    client.get(url)
    #create a new message
    inputMsg = input('Submit a message: ')

    if 'csrftoken' in client.cookies:
        elements = {'key':nextkey, 'message':getRandKey(KEYLENGTH) + inputMsg, 'csrfmiddlewaretoken':client.cookies['csrftoken']}
        post = client.post(url, data = elements, headers = {'Referer' : url})


if len(sys.argv) != 4:
    print(f'need ip, port, and 8-digit key as arguments')
    #gets server ip, server port, and 8-digit key as arguments
    sys.exit(-1)
client(sys.argv[1], sys.argv[2], sys.argv[3])
