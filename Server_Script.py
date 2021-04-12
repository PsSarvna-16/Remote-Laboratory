import socket
from tkinter import *
import time

root = Tk()
root.title("Remote-Lab-Server")

class Socket():

	def __init__(self,port,Interface):
		self.port = port
		self.soc = socket.socket()
		Interface.send("Socket Created..")
		self.name = socket.gethostname()
		self.ip = socket.gethostbyname(self.name)
		self.soc.bind(('',self.port))
		Interface.send(f"\nName : {self.name} \nIP   : {self.ip}\nPort : {self.port}")
		

	def acceptClients(self,count):
		self.soc.listen(count)
		Interface.send("\nWaiting For Clients..")

	def closeCon(self):
		self.soc.close()
		Interface.send("\nSocket Closed !!")

class TkFrame:
	
	def __init__(self,root):
		Main = Frame(root)

		self.text = Text(Main ,width = 40,height = 25,state = DISABLED,background= "#EBEBEB",xscrollcommand = True)
		self.text.grid()

		Main.grid()

	def send(self,msg):
		self.text.config(state = NORMAL)
		self.text.insert(END ,msg + "\n")
		self.text.config(state = DISABLED)


Interface = TkFrame(root)
ser = Socket(6666,Interface)
ser.acceptClients(3)
ser.closeCon()
root.mainloop()