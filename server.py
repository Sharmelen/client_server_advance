import time, socket, sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def pem_reader(keyfile):

	with open(keyfile, "rb") as key_file:
	
		public_key = serialization.load_pem_public_key(
			key_file.read(),
			backend=default_backend()
		)
		return public_key
	
new_socket = socket.socket()
host_name = socket.gethostname()
s_ip = socket.gethostbyname(host_name)
 
port = 8080
 
new_socket.bind((host_name, port))
print("Binding successful!")
#print("This is your IP: ", s_ip)
 
name = "Server"
 
new_socket.listen(1) 
 
 
conn, add = new_socket.accept()
 
print("Received connection from ", add[0])
print('Connection Established. Connected From: ',add[0])
 
client = (conn.recv(1024)).decode()
print(client + ' has connected.')
 
conn.send(name.encode())

while True:
	# message = input('Me : ')
	# conn.send(message.encode())
	message = conn.recv(1024)
	message = message.decode()
	print(message)
	#print(client, ':', message)
	
	split_msg = message.split("#")
	
	if split_msg[1] == "1":
	
		if split_msg[2] == "clientA":
			print("True selection")
			
			f = open("clientA_public_key.txt","rb")
			message = f.read()
			conn.send(message)
			
			message = conn.recv(1024)
			message = message
			print(message.hex())
			f = open("stored_msg","w")
			f.write(split_msg[0]+"#"+str(message.hex())+"#"+split_msg[2])
			f.close()
			
	if split_msg[1] == "2":
		print("Second Option")
		
		f = open("stored_msg","r")
		client_msg = f.read()
		split_c_msg = client_msg.split("#")
		#print(split_c_msg[2])
		if split_c_msg[2] == split_msg[0]:
			msg1 = split_c_msg[0]
			msg2 = split_c_msg[1]
			
			total_msg = msg1+"#"+msg2
			
			conn.send(total_msg.encode())
			
		else:
			msg = "Sorry there is no message"
			conn.send(msg.encode())
			
		
		
			
			
			
			
		
	
	
	