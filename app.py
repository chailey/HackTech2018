import tkinter 
from PIL import ImageTk, Image
import smart_scanner 
import facetest



def go():
	label1 = tkinter.Label(window, text= "Loading ... When the camera comes, hold your product up and press 'q' when ready").pack()
	names = ["Kaushik", "Radhika", "Maegan", "Chris"]
	namesMoney = [20,20,20,20] 
	facetest.deletePersonGroup()
	facetest.createPersonGroup()
	ids = facetest.createPerson(names)
	facetest.trainGroup()
	facetest.getItem() 
	costArr = facetest.itemDetect("https://chrishacktech.blob.core.windows.net/photos/blobItem.jpg")
	cost = facetest.parseCost(costArr) 
	print (cost) 
	if (cost == -1): 
		cost = input("Sorry, number not recognized. Please type in.")
	testImage = facetest.captureImage() 
	foundName = facetest.detectFace(testImage)
	detection = "We detected " + foundName + ". Searching in database..."
	print (detection) 
	label2 = tkinter.Label(window, text= detection)
	i = 0 
	while i < len(names):
		if (names[i] == foundName):
			break 
		i = i + 1  
	if i < len(names):
		costFactor = "Your current bank account balance is " + str(namesMoney[i]) + " . Total cost is " + str(cost)
		print (costFactor)
		label3 = tkinter.Label(window, text= costFactor)
		newBankBalance = int(namesMoney[i]) - int(cost) 
		if (newBankBalance < 0):
			label4 = tkinter.Label(window, text = "Transaction denied. You have no more funds.") 
			print("Transaction denied. You have no more funds.")
		else:
			label5 = tkinter.Label(window, text = "Transaction accepted. Your FacePay balance is now " + str(newBankBalance))
			print("Transaction accepted. Your FacePay balance is now " + str(newBankBalance))
			namesMoney[i] = newBankBalance
	else:
		print ("We couldn't find you. Please try again.")







window = tkinter.Tk()
 
window.title("FacePay")


b1 = tkinter.Button(window, text= "New user")
b1.pack() 

b2 = tkinter.Button(window, text= "Existing user", command = lambda: go())
b2.pack() 
window.mainloop()

