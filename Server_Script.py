#--------------------------------------Modules------------------------------------------------
import socket
from tkinter import *
import time,threading,json
#--------------------------------------Tkinter------------------------------------------------
root = Tk()
root.title("Remote-Lab-Server")
#--------------------------------------Socket------------------------------------------------

def loginAuth(ser):
	ser.sendData("Ok")
	msg = ser.recvData()
	msg = msg.split("%")
	print(msg)
	with open("cred.json", 'r') as f:
		data = json.load(f)
	if msg[0] in data:
		if data[msg[0]]['pwd'] == msg[1]:
			ser.sendData("Ok")
			return
	ser.sendData("Not")

class Socket():

	def __init__(self,port,Interface):
		self.port = port
		self.soc = socket.socket()
		Interface.send("Socket Created..")
		print("Socket Created..")
		self.name = socket.gethostname()
		self.ip = socket.gethostbyname(self.name)
		self.soc.bind(('',self.port))
		Interface.send(f"\nName : {self.name} \nIP   : {self.ip}\nPort : {self.port}")
		print(f"\nName : {self.name} \nIP   : {self.ip}\nPort : {self.port}")
		

	def acceptClients(self):
		self.soc.listen(3)
		while True:
			Interface.send("\nWaiting For Clients..")
			print("\nWaiting For Clients..")
			self.client, self.addr = self.soc.accept()
			Interface.send(f"\nConnected with {self.addr}")
			print(f"\nConnected with {self.addr}")
			self.recvData()
			while True:
				msg = self.client.recv(1024).decode()
				Interface.send(msg)
				if msg == "Login":
					loginAuth(self)
				elif msg == "Exit":
					self.closeCon()
				else:
					Interface.send(msg)

	def sendData(self,msg):
		print("sent : " + msg)
		self.client.send(bytes(msg,'utf-8'))
		return
	
	def recvData(self):
		msg = self.client.recv(1024).decode()
		print("rec  : "+ msg)
		return msg

	def closeCon(self):
		self.soc.close()
		Interface.send("\nSocket Closed !!")
#-------------------------------------TkFrame----------------------------------------------------

class TkFrame:
	
	def __init__(self,root):
		Main = Frame(root)

		self.text = Text(Main ,width = 40,height = 25,state = DISABLED,background= "#EBEBEB",xscrollcommand = True)
		self.text.grid(row=1,columnspan=2)
		global ser
		self.start_b = Button(Main,text= "Start", command = lambda: startCon())
		self.start_b.grid(row=0,column=0)
		self.terminate_b = Button(Main,text = "Terminate",command = lambda:  ser.closeCon())
		self.terminate_b.grid(row=0,column=1)

		Main.grid()

	def send(self,msg):
		self.text.config(state = NORMAL)
		self.text.insert(END ,msg + "\n")
		self.text.config(state = DISABLED)

def startCon():
	global ser
	thread = threading.Thread(target = ser.acceptClients )
	thread.start()
#---------------------------------------Login-----------------------------------------



#--------------------------------------------------------------------------------------
Interface = TkFrame(root)
ser = Socket(6665,Interface)

root.mainloop()
#------------------------------------------END-------------------------------------------
