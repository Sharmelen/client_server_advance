from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import time, socket, sys
 
socket_server = socket.socket()
server_host = socket.gethostname()
ip = socket.gethostbyname(server_host)
sport = 8080
 
print('This is your IP address: ',ip)
server_host = "192.168.77.1"
name = "Server"
 
 
socket_server.connect((server_host, sport))
 
socket_server.send(name.encode())
server_name = socket_server.recv(1024)
server_name = server_name.decode()
 
print(server_name,' has joined...')
while True:

	option = input("Pick An Option \n1. Encrypt\n2. Request File(Decrypt)\n>")
	
	if option == "1":
	
		name = input("Whose public key do you want?\n>")
		msg = input("Enter the message you want to encrypt\n>")
		message = "clientB#"+option+"#"+name
		socket_server.send(message.encode()) 
		message = (socket_server.recv(1024)).decode()
		print(message)
		f = open("public_key.pem","w")
		f.write(message)
		f.close()
		
		with open("public_key.pem", "rb") as key_file:
			public_key = serialization.load_pem_public_key(
				key_file.read(),
				backend=default_backend()
			)
			
		message = msg.encode('utf-8')

		encrypted = public_key.encrypt(
			message,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA256()),
				algorithm=hashes.SHA256(),
				label=None
			)
		)
		
		socket_server.send(encrypted)
		
	elif option == "2":
		message = "clientA#"+option
		socket_server.send(message.encode()) 
		message = (socket_server.recv(1024)).decode()
		if "#" in message:
			msg_split = message.split("#")
			msg_from = msg_split[0]
			
			with open("clientA_private_key.pem", "rb") as key_file:
				private_key = serialization.load_pem_private_key(
					key_file.read(),
					password=None,
					backend=default_backend()
				)
			
			encrypted =  bytes.fromhex(msg_split[1]) 

			original_message = private_key.decrypt(
				encrypted,
				padding.OAEP(
					mgf=padding.MGF1(algorithm=hashes.SHA256()),
					algorithm=hashes.SHA256(),
					label=None
				)
			)
			print()
			print("Looks Like You Do Have A Message")
			print(msg_from)
			print(original_message)
			print()
				
		
		
		
		
		
		
    # message = (socket_server.recv(1024)).decode()
    # print(server_name, ":", message)
    # message = input("Me : ")
    # socket_server.send(message.encode())  
