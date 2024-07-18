import pywhatkit

phone=input("Enter phone number: ")
path='Textout.txt'
with open(path,'r') as file:
  content=file.read()

pywhatkit.sendwhatmsg_instantly(phone,content,10)