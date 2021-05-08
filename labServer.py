#--------------------------------------Modules------------------------------------------------
import socket,time
from pyfirmata import Arduino,util, STRING_DATA
from tkinter import *
from random import randint
import time,threading,json

#--------------------------------------Tkinter------------------------------------------------
root = Tk()
root.title("Remote-Lab-Server")
root.iconbitmap(r'Image.ico')
#--------------------------------------Socket------------------------------------------------

class Ardino:

	def __init__(self):
		pass

	def connectArd(self):
		try:
			self.board.exit()
		except:
			pass
		self.board = Arduino('COM3')
		self.lcd(" ")
		self.ser = self.board.get_pin('d:6:s')
		return

	def lcd(self,text):
	    if text:
	        self.board.send_sysex( STRING_DATA, util.str_to_two_byte_iter( text ))
	    return

	def servo(self,val):
		self.ser.write(int(val))
		self.lcd(str(val))
		return

	def disconnectArd(self):
		try:
			self.ser.write(int(0))
			self.lcd(str(0))
			self.lcd("S")
			sleep(2)
			self.board.exit()
			return
		except:
			pass

class Socket:

	def __init__(self,port):
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
		Interface.send("\nWaiting For Clients..")
		print("\nWaiting For Clients..")
		self.client, self.addr = self.soc.accept()
		Interface.send(f"\nConnected with {self.addr}")
		print(f"\nConnected with {self.addr}")
		self.recvData()
		while self.client:
			try:
				msg = self.client.recv(1024).decode()
				if msg == "ConnectArduino":
					Interface.send(f"\n******Servo  Connected******")
					ard.connectArd()
				elif msg == "DisConnectArduino":
					Interface.send(f"\n*****Servo DisConnected*****")
					ard.disconnectArd()
				elif msg[0] == 'S':
					Interface.send(f"\nPosition : " + msg[1:])
					ard.servo(int(msg[1:]))
				elif msg == "Back":
					ard.disconnectArd()
				elif msg == "Exit":
					ard.disconnectArd()
					self.closeCon()
					break
				else:
					Interface.send(msg)
			except Exception as e:
				print(e)

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
		try:
			self.client.close()
		except:
			pass
		try:
			self.soc.close()
			Interface.send("\nSocket Closed !!")
		except:
			pass
		try:
			ard.disconnect()
			Interface.send("\nArduino Closed !!")
		except:
			pass
#-------------------------------------TkFrame----------------------------------------------------

class TkFrame:
	
	def __init__(self,root):
		Main = Frame(root)
		global ser
		self.text = Text(Main ,width = 40,height = 25,state = DISABLED,background= "#EBEBEB",xscrollcommand = True)
		self.text.grid(row=1,columnspan=2)
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

	ser = Socket(port)
	ser.startCon()
	thread = threading.Thread(target = ser.acceptClients )
	thread.start()
#--------------------------------------------------------------------------------------

Interface = TkFrame(root)
ard = Ardino()
port= 5000

try:
	ser = Socket(port)
except:
	pass

root.mainloop()
#------------------------------------------END-------------------------------------------