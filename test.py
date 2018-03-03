########### Python 2.7 #############
import requests, json, urllib.request, urllib.parse, urllib.error

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '1f3021aa1ab74cedaf685826f631ab5a',
}

def detectFace(): 
    urlAPI = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?' + urllib.parse.urlencode({ 'returnFaceId': 'true'}) 
    body = { "url" : "https://scontent-lax3-1.xx.fbcdn.net/v/t31.0-8/18595423_1720002141634025_1533763974652478544_o.jpg?oh=b720f6bde1d2226661bbd757a82d5f1d&oe=5B45CAF0"}
    response = requests.post(url = urlAPI, json = body, headers = headers)
    print(response.json()[0]["faceId"])


detectFace()