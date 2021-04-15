import smtplib
from random import randint
from email.message import EmailMessage

class Mail:
	EMAIL_ADDR = ""
	EMAIL_PWD = ""

	def __init__(self,mail,pwd):
		self.EMAIL_ADDR = mail
		self.EMAIL_PWD = pwd

	def sendMail(self,mail,subj,body):
		msg = EmailMessage()
		msg['Subject'] = subj
		msg['From'] = self.EMAIL_ADDR
		msg['To'] = mail
		msg.set_content(body)
		try:
			with smtplib.SMTP('smtp.gmail.com',587) as smtp:
				smtp.starttls()
				smtp.login(self.EMAIL_ADDR,self.EMAIL_PWD)
				smtp.send_message(msg)
				return 1
		except Exception as e:
			return e


"""
from SendMail import *

gmail = Mail("pssaravna.kumar@gmail.com","Pss@160499")

gmail.sendMail("sarvna.ps@gmail.com","Python","Generated Mail")

"""