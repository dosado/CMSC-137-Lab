import socket
import threading 
#import server

#initialized variables as per learning
HEADER = 500
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.1.4"
addr = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
result_frm_comparison,final = None, None


#start of socket for client file
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)

 
#loop to recieve and send data to server until connection becomes False
connected = True
while connected:
    
    #receives threaded message from client to start the game/every round
    msg = client.recv(HEADER).decode(FORMAT)
    print(msg)
    #checks for winning and losing messages to end the loop and the program
    if msg == "Congratulations, You won!" or msg == "Sorry, try again next time!":
        print(msg, "YESSSS")
        connected = False

    else:
        player_choice = input("Jack-En-Poy, make your choice: ")
        print("[AWAITING OTHER PLAYER'S HAND...]")
        print("NWHATT")
        #choices are sent to the server side
        client.send(player_choice.encode(FORMAT))

