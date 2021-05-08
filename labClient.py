#--------------------------------------Modules------------------------------------------------

import socket,time
from tkinter import *
from tkinter import messagebox

#--------------------------------------Tkinter------------------------------------------------
root = Tk()
root.title("Remote-Laboratory")
root.geometry("430x400")
root.iconbitmap(r'Image.ico')
#--------------------------------------functions------------------------------------------------

def closeSer():
	global cli
	if(messagebox.askyesno(f"Warning", "Want to Exit?")):
		try:
			cli.sendData("Exit")
			sleep(2)
			cli.con.close()
			exit()
		except:
			exit()

def connect(frame):
	stat = frame.conn_S.cget('text')
	print(stat)
	global cli
	if stat == "Connect":
		cli.sendData("ConnectArduino")
		frame.conn_S.config(text = "DisConnect")
	else:
		cli.sendData("DisConnectArduino")
		frame.conn_S.config(text = "Connect")
	return

def writeServo(frame):
	val = frame.otp_S.get()
	cli.sendData("S" + val)
	return

def onlyDigit(dig):
	if re.search("[0-9]$",dig) and len(str(dig)) <= 3:
		return True
	elif dig == "":
		return True
	return False
	
#--------------------------------------Socket------------------------------------------------

class Socket():

	def __init__(self,ip,port):
		self.ip = ip
		self.port = port

	def connectServer(self):
		self.con = socket.socket()
		print("ok")
		self.con.connect((self.ip,self.port))
		print("ok")
		self.sendData("Ok")
		print("ok")
		return

	def sendData(self,msg):
		print("sent : " + msg)
		self.con.send(bytes(msg,'utf-8'))
		return
	
	def recvData(self):
		msg = self.con.recv(1024).decode()
		print("rec  : "+ msg)
		return msg

#--------------------------------------TkFrame------------------------------------------------


class TkFrame:
	
	def __init__(self,root):
		pass

	def experiments(self,root):

		root.geometry("430x350")
		self.exp_f = Frame(root,width = 430,height=350,bg= "#0A2472")
		self.exp_f.place(x=0,y=0)

		Label(self.exp_f,text= "experiments",fg= "white",bg= "#0A2472",font = ("Engravers MT",16)).place(x=120,y=30,width=200,height=40)

		self.ser_b = Button(self.exp_f, text ="SERVO MOTOR CONTROL",fg="black",bg="#32A6C3",font = ("Georgia",8) ,command = lambda: self.bringServo(root))
		self.ser_b.place(x=150,y=100,width=150,height=30)

		self.exit_L = Button(self.exp_f, text ="EXIT",fg="black",bg="#FAA34C",font = ("Georgia",8)  ,command = lambda: closeSer())
		self.exit_L.place(x=35,y=300,width=100,height=30)

		self.exp_f.place_forget()

	def servoMotor(self,root):
		
		root.geometry("430x350")
		self.ser_f = Frame(root,width = 430,height=350,bg= "#0A2472")
		self.ser_f.place(x=0,y=0)

		Label(self.ser_f,text= "SERVO MOTOR",fg= "white",bg= "#0A2472",font = ("Engravers MT",16)).place(x=115,y=15,width=200,height=40)
		
		self.conn_S = Button(self.ser_f, text ="Connect" ,fg="black",bg="cyan",font = ("Georgia",12),command =lambda: connect(self))
		self.conn_S.place(x=175,y=100,width=80,height=25)

		self.slider = Scale(self.ser_f,from_ = 0, to = 180,highlightbackground = "#0A2472",bg= "#0A2472",fg="white",orient = HORIZONTAL)
		self.slider.place(x=120,y=150,width = 120)

		self.otp_S = Entry(self.ser_f,width = 3,background= "#EBEBEB",text= "OTP")
		self.otp_S.place(x=260,y=170,width=30,height=20)		

		digit = root.register(onlyDigit)

		self.otp_S.config(validate = "key",validatecommand = (digit,'%P'))

		self.upd_S = Button(self.ser_f, text ="Update" ,fg="black",bg="cyan",font = ("Georgia",12),command =lambda: writeServo(self))
		self.upd_S.place(x=175,y=220,width=80,height=25)

		self.back_S = Button(self.ser_f, text ="Back" ,fg="black",bg="#FAA34C",font = ("Georgia",8),command =lambda: self.bringExperiments(root))
		self.back_S.place(x=50,y=300,width=65,height=27)

		self.ser_f.place_forget()

	def bringExperiments(self,root):
		self.ser_f.place_forget()
		root.geometry("430x350")
		self.exp_f.place(x=0,y=0)	

	def bringServo(self,root):
		self.exp_f.place_forget()
		root.geometry("430x350")
		self.ser_f.place(x=0,y=0)

#--------------------------------------------------------------------------------------------

window = TkFrame(root)
window.experiments(root)
window.servoMotor(root)
window.bringExperiments(root)

try:
	cli = Socket('192.168.43.180',5000)
	print("ok")
	cli.connectServer()
except Exception as e:
	messagebox.showerror(f"Warning", e)

root.mainloop()
#--------------------------------------END------------------------------------------------