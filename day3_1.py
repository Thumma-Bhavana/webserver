import socket
import os
from pathlib import Path
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip = ''
port = 1234
temp = ""
def goto():
	temp=os.getcwd()
	dirl = os.listdir()
	content ="Select files"
	content+="<ul>"
	for i in dirl:
		# if(os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/"+i)):
		# 	fin = open(i)
		# 	content = fin.read()
		# 	fin.close()	
		# elif(os.path.isdir(os.path.dirname(os.path.realpath(__file__))+"/"+i)):
		# 	d = os.path.dirname(os.path.realpath(__file__))
		# 	content+="\n"+"<a href="+d+'/'+i+">"+i+"</a>"
		d = temp
		content+="<li><a href="+d+'/'+i+">"+i+"</a></li>"
	content+="</ul>"
	return content
print("<<<<<<< Server started >>>>>")
soc.bind((ip, port))
print(f"Port:{port}")
soc.listen(1)
while(True):
	conn, addr = soc.accept()
	request = conn.recv(1024)
	print(request.decode('utf-8'))
	lines = request.decode('utf-8').split('\n')
	filename = lines[0].split()[1]
	if( filename == '/'):
		filename =os.path.dirname(os.path.realpath(__file__))+"/index.html"
	try:
		l=["html", "txt", "pdf", "image"]
		if(filename == "/log"):
			content ="<CENTER><h1>Forbidden Page<h1><CENTER>"
			response ="HTTP/1.1 403 FORBIDDEN\nContent-Type: text/html\n\n"+content
		elif("." in filename and filename.split(".")[1] not in l):
			content ="<CENTER><h1>Unsupported Media Type<h1><CENTER>"
			response ="HTTP/1.1 415 MEDIATYPE\nContent-Type: text/html\n\n"+content
		else:
			print("**************"+filename+"************")
			if(os.path.isdir(filename)):
				if(filename.split("/")[-1] != 'index.html'):
					os.chdir(filename)
				print("Entered GOTO")
				content = goto()
				response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'+content
			elif(filename.split("/")[-1] in os.listdir() and os.path.isfile(filename)):
				print("***************READ THE FILE*******************")
				print(filename.split("/")[-1])	
				fin = open(filename.split("/")[-1])
				content = fin.read()
				fin.close()
				response ="HTTP/1.1 200 OK\nContent-Type: text/html\n\n"+content
			else:
				raise FileNotFoundError
	except FileNotFoundError:
		
		if(filename.split("/")[-1] == "index.html"):
			content = goto()
			response = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'+content
		else:
			content ="<CENTER><h1>File Not Found<h1><CENTER>"
			response = 'HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n'+content

	conn.sendall(response.encode())
	conn.close()
print("Done!!!")
soc.close()




