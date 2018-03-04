import requests
import json
import cv2
import boto3
import boto.s3.connection
import boto

key = '4a06edca17014688b808c4318d99a0ca'
headers= {"Host": 'westcentralus.api.cognitive.microsoft.com', "Content-Type":'application/json','Ocp-Apim-Subscription-Key': key }

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

def rekognition(image):
	bucket='rekognition-examples-bucket-hacktech'
	#add updated image to bucket
	conn = boto.s3.connect_to_region('us-east-1', aws_access_key_id = 'AKIAIJZ44BAFK3KAIZRA', aws_secret_access_key = 'AMi3XpJniSQ3LIR3c7t4YFf2Ehq6Ile9AG7/xh4+',calling_format = boto.s3.connection.OrdinaryCallingFormat(),)
	tempBucket = conn.get_bucket(bucket)
	key_name = image;
	k = tempBucket.new_key(key_name)
	k.set_contents_from_filename(key_name)

	client = boto3.client('rekognition','us-east-1')
	fileName=image
	#get image from bucket
	response = client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})
	words = []
	for i in range(len(response["TextDetections"])):
		word = response["TextDetections"][i]["DetectedText"]
		if(any(j.isdigit() for j in word)): #nothing with a number is being stored
			continue
		word = str(word).lower()
		if word not in words and len(word) > 2: #dont want short words like a or as
			words.append(word)
			print(word)


imageName = captureImage()
rekognition(imageName)

