import socket
from tkinter import *

root = Tk()
root.title("Remote-Lab-Server")


class Socket():
	name = ""
	ip = ""
	port = ""
	soc = ""

	def __init__(self,port):
		self.soc = socket.socket()
		self.name = socket.gethostname()
		self.ip = socket.gethostbyname(name)
		self.soc.bind(('',port))
		self.soc.listen(1)


class TkFrame:
	
	def __init__(self,root):
		Main = Frame(root)

		self.text = Text(Main ,width = 40,height = 30,background= "#EBEBEB")
		self.text.grid()

		Main.grid()


Interface = TkFrame(root)
root.mainloop()