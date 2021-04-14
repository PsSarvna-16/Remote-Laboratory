#--------------------------------------Modules------------------------------------------------
import socket
from tkinter import *
from tkinter import messagebox
#--------------------------------------Tkinter------------------------------------------------

root = Tk()
root.title("Remote-Laboratory")
root.geometry("430x400")
root.iconbitmap(r'Image.ico')
#--------------------------------------functions------------------------------------------------

def authLogin(frame):
	global cli
	user = frame.user_L.get().strip()
	pwd = frame.pwd_L.get().strip()

	msg = "Login"
	cli.sendData(msg)
	if(cli.recvData()) == "Ok":
		msg = user + "%" + pwd
		cli.sendData(msg)
		if(cli.recvData()) == "Ok":
			messagebox.showinfo(f"Succes", "Logged-In")
			return 1
	messagebox.showwarning(f"Warning", "Credentials Not MAtched")

def closeSer():
	global cli
	if(messagebox.askyesno(f"Warning", "Want to Exit?")):
		try:
			cli.sendData("Exit")
			cli.con.close()
			exit()
		except:
			exit()

#--------------------------------------Socket------------------------------------------------

class Socket():

	def __init__(self,ip,port):
		self.ip = ip
		self.port = port

	def connectServer(self):
		self.con = socket.socket()
		self.con.connect((self.ip,self.port))
		self.sendData("Ok")
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

	def Login(self,root):

		self.Login_f = Frame(root,width = 430,height=350,bg= "#0A2472")
		self.Login_f.place(x=0,y=0)

		Label(self.Login_f,text= "Remote Login",fg= "white",bg= "#0A2472",font = ("Engravers MT",14)).place(x=125,y=30,width=200,height=40)

		self.user_L = Entry(self.Login_f,width = 15,fg= "#0B0B0A",text= "User Id",background= "#CEEAF3")
		self.user_L.place(x=150,y=100,width=150,height=25)
		self.user_L.insert(END,"Username")

		self.pwd_L = Entry(self.Login_f,width = 15,fg = "#0B0B0A",show= "*",background= "#CEEAF3")
		self.pwd_L.place(x=150,y=140,width=150,height=25)
		self.pwd_L.insert(END,"Password")

		self.rem_L = Checkbutton(self.Login_f,text= "Remember Me",fg= "white",bg= "#0A2472")
		self.rem_L.place(x=170,y=180)

		self.login_L = Button(self.Login_f, text ="LOGIN",fg="black",bg="#32A6C3",font = ("Georgia",16) ,command = lambda: authLogin(self))
		self.login_L.place(x=150,y=220,width=150,height=30)

		self.sign_L = Button(self.Login_f, text ="SIGN UP" ,fg="white",bg="#0A2472",font = ("Georgia",10),command =lambda: self.bringSignUp(root))
		self.sign_L.place(x=225,y=300,width=150,height=30)
		
		self.exit_L = Button(self.Login_f, text ="EXIT",fg="black",bg="#FAA34C",font = ("Georgia",8)  ,command = lambda: closeSer())
		self.exit_L.place(x=35,y=300,width=100,height=30)

		self.Login_f.place_forget()

	def signUp(self,root):
		
		root.geometry("430x400")
		self.signUp_f = Frame(root,width = 430,height=400,bg= "#0A2472")
		self.signUp_f.place(x=0,y=0)

		Label(self.signUp_f,text= "SIGN UP",fg= "white",bg= "#0A2472",font = ("Engravers MT",18)).place(x=150,y=15,width=130,height=40)
		
		self.namel_S = Label(self.signUp_f,text= "First Name",fg= "white",bg= "#0A2472",font = ("Fixedsys",4))
		self.namel_S.place(x=50,y=65,width=80,height=10)

		self.name_S = Entry(self.signUp_f,width = 15,background= "#EBEBEB")
		self.name_S.place(x=50,y=80,width=150,height=25)
	
		self.regl_S = Label(self.signUp_f,text= "Reg No",fg= "white",bg= "#0A2472",font = ("Fixedsys",4))
		self.regl_S.place(x=222,y=62,width=65,height=15)

		self.reg_S = Entry(self.signUp_f,width = 15,background= "#EBEBEB")
		self.reg_S.place(x=230,y=80,width=150,height=25)

		self.lemail_S = Label(self.signUp_f,text= "E-Mail",fg= "white",bg= "#0A2472",font = ("Fixedsys",4))
		self.lemail_S.place(x=50,y=110,width=50,height=15)

		self.email_S = Entry(self.signUp_f,width = 15,background= "#EBEBEB")
		self.email_S.place(x=50,y=125,width=330,height=25)

		self.pwdl_S = Label(self.signUp_f,text= "Password",fg= "white",bg= "#0A2472",font = ("Fixedsys",4))
		self.pwdl_S.place(x=50,y=160,width=65,height=10)

		self.pwd_S = Entry(self.signUp_f,width = 15,background= "#EBEBEB",text= "Password",show= "*")
		self.pwd_S.place(x=50,y=175,width=150,height=25)

		self.cpwdl_S = Label(self.signUp_f,text= "Confirm Password",fg= "white",bg= "#0A2472",font = ("Fixedsys",4))
		self.cpwdl_S.place(x=222,y=160,width=150,height=10)

		self.cpwd_S = Entry(self.signUp_f,width = 15,background= "#EBEBEB",text= "Confirm Password",show= "*")
		self.cpwd_S.place(x=230,y=175,width=150,height=25)
		
		self.otpb_S = Button(self.signUp_f, text ="GET OTP" ,command = lambda: closeSer())
		self.otpb_S.place(x=175,y=225,width=80,height=20)	

		self.otp_S = Entry(self.signUp_f,width = 15,background= "#EBEBEB",text= "OTP")
		self.otp_S.place(x=175,y=255,width=80,height=20)	

		self.sign_S = Button(self.signUp_f, text ="CREATE ACCOUNT",fg="black",bg="#32A6C3",font = ("Georgia",8)  ,command = lambda: closeSer())
		self.sign_S.place(x=150,y=285,width=130,height=30)

		self.back_S = Button(self.signUp_f, text ="Back" ,fg="black",bg="cyan",font = ("Georgia",8),command =lambda: self.bringLogin(root))
		self.back_S.place(x=50,y=335,width=60,height=25)

		self.signUp_f.place_forget()
		
	def bringLogin(self,root):
		self.signUp_f.place_forget()
		root.geometry("430x350")
		self.Login_f.place(x=0,y=0)	

	def bringSignUp(self,root):
		self.Login_f.place_forget()
		root.geometry("430x400")
		self.signUp_f.place(x=0,y=0)
#--------------------------------------------------------------------------------------------

window = TkFrame(root)
window.Login(root)
window.signUp(root)
window.bringLogin(root)
try:
	cli = Socket('192.168.43.179',6665)
	cli.connectServer()
except Exception as e:
	messagebox.showerror(f"Warning", e)

root.mainloop()
#--------------------------------------END------------------------------------------------
