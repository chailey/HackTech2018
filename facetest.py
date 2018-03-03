#change back to python 3.6 later (only changes involve urllib)
import requests
import json
#import urllib.request, urllib.parse, urllib.error
import urllib, urllib2
#hard coded values
key = "ba2011a89a13483fab1390e169ea5173"
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
def createPerson():
	url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+personGroupId+"/persons"
	#hardcoded names
	names = ["Kaushik", "Radhika", "Maegan", "Chris"]
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
	urlAPI = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?' + urllib.urlencode({ 'returnFaceId': 'true'})
	#photo to check
	body = { "url" : imageUrl}
	response = requests.post(url = urlAPI, json = body, headers = headers)
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

deletePersonGroup()
createPersonGroup()
ids = createPerson()
trainGroup()
testImage = "https://scontent-lax3-1.xx.fbcdn.net/v/t1.0-9/14642115_641584432676580_1901022073400796775_n.jpg?oh=a947a2d12b532ee9cd2a3b5bebbd235f&oe=5B012EB4"
print ("Detected face", detectFace(testImage))