#change back to python 3.6 later (only changes involve urllib)
import requests
import json
import urllib.request, urllib.parse, urllib.error
import cv2
#import urllib, urllib2
#hard coded values
key = "1f3021aa1ab74cedaf685826f631ab5a"
headers= {"Host": 'westcentralus.api.cognitive.microsoft.com', "Content-Type":'application/json','Ocp-Apim-Subscription-Key': key }
personGroupId = "test123"

#create person group
def createPersonGroup():
	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+ personGroupId
	#not used elsewhere
	personGroupDisplayName = "My Group"

	body = { "name": personGroupDisplayName }

	response = requests.put(url=url,json=body,headers=headers)
#delete person group removes everything related to it
def deletePersonGroup():
	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/" + personGroupId
	response = requests.delete(url=url,headers=headers)
#takes in the user's id, gets their name, and adds a photo from an url
def addFace(personID):
	name = getPersonName(personID)

	if(name == 'Kaushik'):
		photo = 'https://media.licdn.com/dms/image/C5103AQF6o6kmZyN5qQ/profile-displayphoto-shrink_200_200/0?e=1525255200&v=alpha&t=qSE3eKdrVZkrpMpWnS9ldheYY7t0NF1E6d2wbkL3ig8'
	elif(name == 'Radhika'):
		photo = 'https://scontent-lax3-1.xx.fbcdn.net/v/t31.0-8/22859851_833930706775284_2298164206331624972_o.jpg?oh=da14e9f5d3f6dd67ed16ac6b5d49ca23&oe=5B49CFC2'
	elif(name == 'Maegan'):
		photo = 'https://scontent-lax3-1.xx.fbcdn.net/v/t31.0-8/18839535_710270525842729_6235509578421077480_o.jpg?oh=812bc4ca650131295a23e089e02c7f3b&oe=5B442168'
	elif(name == 'Chris'):
		photo = 'https://scontent-lax3-1.xx.fbcdn.net/v/t31.0-8/21457362_1762418087392430_5728002921223690541_o.jpg?oh=1e62faa1f514bef393fb4a5e5cf3830d&oe=5B4BFA1C'

	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+personGroupId+"/persons/"+personID+"/persistedFaces"
	data = {"url":photo}
	requests.post(url=url,json=data,headers=headers)

#create person group person (including faces). returns list of ids of created people
def createPerson(names):
	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+personGroupId+"/persons"
	#hardcoded names
	#names = ["Kaushik", "Radhika", "Maegan", "Chris"]
	ids = []
	for name in names:
		body = { "name": name }
		response = requests.post(url=url,json=body,headers=headers)
		try:
			tempID = str(response.json()["personId"])
		except:
			print("createPerson rate limited")
		ids.append(tempID)
		addFace(tempID)
	return ids

#deletes a person from their person id
def deletePerson(personID):
	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+personGroupId+"/persons/"+personID
	response = requests.delete(url=url,headers=headers)

def getPersonName(personID):
	getURL = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/" + personGroupId + "/persons/" + personID
	response = requests.get(url=getURL,headers=headers)
	try:
		name = response.json()["name"]
	except:
		print("getPersonName rate limited")
	return name
def trainGroup():
	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+personGroupId+"/train"
	response = requests.post(url=url, headers=headers)
def detectFace(imageUrl): 
	localHeaders = {"Host": 'westcentralus.api.cognitive.microsoft.com', "Content-Type":'application/octet-stream','Ocp-Apim-Subscription-Key': key }
	urlAPI = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?' + urllib.parse.urlencode({ 'returnFaceId': 'true'})
	#photo to check
	data = open(imageUrl, 'rb').read()  
	#body = { "url" : imageUrl}
	response = requests.post(url = urlAPI, data = data, headers = localHeaders)
	print (response.json())
	try:
		theirID = response.json()[0]["faceId"]
	except:
		print("rate limits suck")

	faceIDs = [theirID]
	identifyURL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/identify'
	body = {"personGroupId":personGroupId,"faceIds":faceIDs,"maxNumOfCandidatesReturned": 1,"confidenceThreshold": 0.5}
	response = requests.post(url = identifyURL, json = body, headers = headers)
	try:
		winner = response.json()[0]['candidates'][0]['personId']
	except:
		print("rate limited")
	return getPersonName(winner)


def itemDetect(imageUrl): 
	handWriteDetectKey = "85f3d93125ad42b78b08b6a9e5c5f240"
	url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/recognizeText?handwriting=true"
	detectHeaders = {"Content-Type":'application/json','Ocp-Apim-Subscription-Key': handWriteDetectKey}
	data = {"url": imageUrl}
	response = requests.post(url = url, json = data, headers = detectHeaders) 
	#operationLocation =  response.headers['Operation-Location'];
	operationLocation = response.request.headers['Operation-Location']
	operationID = str(operationLocation)[operationLocation.rfind('/')+1:]

	import time
	#sometimes takes a second to process
	time.sleep(1)

	tempUrl = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/textOperations/'+operationID
	response = requests.get(url=tempUrl,headers=detectHeaders)

	recognitionResult = response.json()['recognitionResult']
	if(len(str(recognitionResult)) == 0):
		return -1;
	val = recognitionResult['lines'][0]['text']
	return val


def captureImage(): 
	cap = cv2.VideoCapture(0)

	while(True):
		ret, frame = cap.read()
		if ret is True: 
			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
		else:
			continue 
		cv2.imshow('frame', rgb)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			picName = 'capture.jpg'
			out = cv2.imwrite(picName, frame)
			cap.release()
			cv2.destroyAllWindows()
			return picName


itemDetect("https://chrishacktech.blob.core.windows.net/photos/price8.jpg")

#names = ["Kaushik", "Radhika", "Maegan", "Chris"]
#namesMoney = [20,20,20,20] 
#deletePersonGroup()
#createPersonGroup()
#ids = createPerson(names)
#trainGroup()
#testImage = captureImage() 
#foundName = detectFace(testImage)
#print ("We detected " + foundName + ". Searching in database...")
#i = 0 
#while i < len(names):
#	if (names[i] == foundName):
#		break 
#	i = i + 1  

#cost = 4
#if i < len(names):
#	print ("Your current bank account balance is " + str(namesMoney[i]) + " . Total cost is " + str(cost) + ". Tap button to proceed.") 
#else:
#	print ("We couldn't find you. Please try again.")







