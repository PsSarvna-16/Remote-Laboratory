#--------------------------------------Modules------------------------------------------------
import socket
import bcrypt
from SendMail import *
from tkinter import *
from random import randint
import time,threading,json

#--------------------------------------Tkinter------------------------------------------------

root = Tk()
root.title("Remote-Lab-Server")
root.iconbitmap(r'Image.ico')

#--------------------------------------Socket------------------------------------------------

def loginAuth(ser):
	ser.sendData("Ok")
	reg = ser.recvData()
	ser.sendData("Ok")
	pwd = bytes(ser.recvData(),'utf-8')
	print(reg + " " + str(pwd))
	Interface.send(f"Username : " + reg)
	Interface.send(f"Password : " + len(pwd)*"*")
	with open("cred.json", 'r') as f:
		data = json.load(f)
	if reg in data:
		if bcrypt.checkpw(pwd,bytes(data[reg]['pwd'],'utf-8')):
			Interface.send(f"**** Login Sucessfull ****")
			Interface.send(f"-------------------------------")
			ser.sendData("Ok")
			return
	Interface.send(f"**** Login Failed ****")
	Interface.send(f"-------------------------------")
	ser.sendData("Not")

def sendOTP(ser):
	print("inside sendOTP")
	global Email
	ser.sendData("Ok")
	msg = ser.recvData()
	name,mail = msg.split("%")
	print(msg)
	otp = randint(100000,999999)
	subj = f"Remote Login OTP [{otp}]"
	body = "Dear " + name + ",\n Your One Time Password for Remote Login Tce Laboratory is " + str(otp) +"."
	Email.sendMail(mail,subj,body)
	ser.sendData(str(otp))
	reg = ser.recvData()
	pwd = ser.recvData()
	with open("cred.json", 'r') as f:
		data = json.load(f)
	ndata =  { 'name' : name,'id' : reg ,'pwd' : pwd ,'email':mail}
	data[reg] = ndata
	with open("cred.json", 'w') as f:
		json.dump(data, f)
	ser.sendData("Ok")

class Socket():

	def __init__(self,port,Interface):
		self.port = port
		
	def startCon(self):
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
				if msg == "Login":
					Interface.send(f"\n---------Login-----------")
					loginAuth(self)
				elif msg == "OTP":
					sendOTP(self)
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

	def recvByte(self):
		msg = self.client.recv(1024)
		print("rec  : "+ str(msg))
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
	try:
		ser.closeCon()
	except:
		pass
	ser.startCon()
	thread = threading.Thread(target = ser.acceptClients )
	thread.start()

#--------------------------------------------------------------------------------------

Interface = TkFrame(root)
ser = Socket(6666,Interface)
Email = Mail("remotelabtce2021@gmail.com","Ecetce2021")

root.mainloop()
#------------------------------------------END-------------------------------------------