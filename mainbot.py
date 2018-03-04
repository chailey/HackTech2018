import facetest 
import random
import time


def newUserOrientation():
	nameInput = input("Ok, please give me your name")
	numberInput = input("And please give me your number too [10-digits please]")
	names.append(nameInput)
	namesMoney.append(20.00)
	namesNumbers.append(numberInput)
	facetest.createPerson(names)
	print("Ok, smile for the camera and press 'q' when ready!")
	facetest.trainGroup()
	print ("Ok, please wait. Due to legal restrictions, we can only call have 20 API calls a minute.")
	time.sleep(60)
	print ("You may now proceed")




facetest.createPersonGroup()
names = ["Kaushik Tandon", "Radhika Agrawal", "Maegan Chew", "Chris Hailey"]
namesMoney = [20.00,20.00,20.00,20.00] 
namesNumbers = ["4088910387", "6506563747", "5714251850", "4083488437"]

existingUser = ['existing', 'exist', 'Existing', 'existing user', 'Existing user', 'Existing User', 'E', 'e']
newUser = ['new', 'New', 'new user', 'New user', 'New User', 'N', 'n']


userInput = input("Are you a new user or existing user?")

if (userInput in newUser): 
	newUserOrientation()
else:
	facetest.createPerson(names)
	facetest.trainGroup()
	
while True:
	numItems = input("Tell me, how many items are you looking to buy today?")
	items, prices = facetest.processItems(numItems)
	cost = facetest.determineCost(prices)
	print ("Press q to take a picture of yourself")
	personImage = facetest.captureImage()
	foundName = facetest.detectFace(personImage)
	print ("Is that you, " + foundName + "?")
	i = 0
	while i < len(names):
		if(names[i] == foundName):
			break 
		i = i + 1 
	if i <= len(names):
		if (i == len(names)):
			i = i - 1 
		print("Here is your receipt: ")
		facetest.processReceipt(items, prices)
		print ("Here is your total balance: " + str(namesMoney[i]))
		newBankBalance = float(namesMoney[i]) - float(cost) 
		
		if (newBankBalance < 0):
			newBankBalance = 0
		if (newBankBalance == 0):
			print ("Please keep in mind that you are broke. You cannot afford whatever you are buying. This session has now terminated")
			break 
		else:
			userDet = input("Your final balance is " + str(newBankBalance) + ". Would you like to complete the transaction? [Y/N]")
			if (userDet == "Y"):
				print("Transaction accepted. Your FacePay balance is now " + str(newBankBalance))
				namesMoney[i] = newBankBalance
			else:
				print ("This session has ended.")
				break 
	else:
		print("Sorry, we couldn't find you. Please try again")

	userDetermine = input("This session has ended. Do you wish to continue? [Y/N]")
	if (userDetermine != "Y"):
		break 



