import socket
import threading 



HEADER = 500
PORT = 5050 
#SERVER = "192.168.1.14"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
listofclient = {}
clientconn = []
inputs = {}
#no_winner = True

Score_p1 = 0
Score_p2 = 0


print(SERVER)
print(socket.gethostname())

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM )
server.bind(ADDR)

#function to handle the client's connection (most of the process happens here)
def handle_client(conn, addr):
    print(f"[New COnnection] {addr} connecteddd")
    #send prompt message to client
    prompt = """ MAKE YOUR MOVE 
            R = Rock
            P = paper
            S = SCISSORS
            """
    conn.send(prompt.encode(FORMAT))
    
    #receive message from client
    msg = conn.recv(HEADER).decode(FORMAT)

    print(f"Player {addr} has chosen {msg}!")
    #append client's reponse to list of inputs
    inputs[addr] = msg
 

#function that happens when a client connects
def start():
    server.listen(2)    #servers allows only 2 client connections
    print(f"[LISTENING] server is listening on {SERVER}")
    
    #check number of connected clietns
    while (len(clientconn)<2):
        conn, addr = server.accept()    #accept connections
        print(f"Player {len(clientconn)+1} has entered at {addr}")
        print(addr[1], "port of connection")
        
        #APPEND CLIENT DETAILS to LISt
        clientconn.append(conn)

        print("current number of players:", len(clientconn))

    #While Loop runs the game flow
    while True:
        #inputs list are initialized
        inputs[0] = 0
        inputs[1] = 0

        #CHECKER for Winnign Player
        if (Score_p1 >= 3 or Score_p2 >= 3):
            break   #STOPS LOOP IF MAY WINNER/meets conditions
        else:
            #STARTS 2 separate threads (AS You can notice, clientconn[0] and clientconn[1])
            thread1 =  threading.Thread(target=handle_client, args=(clientconn[0],0))
            thread1.start()
            
            thread2 =  threading.Thread(target=handle_client, args=(clientconn[1],1))
            thread2.start()
            
            thread1.join()
            thread2.join()
            print(f"[ACTIVE connections] {len(clientconn)}")
            #listofclient[(threading.active_count() - 1)] = str(addr[1])

            #Starts the game function
            game()

    #when loop in the Game function ends it proceeds to here
    # Checks which player score reach the winning points
    if Score_p1 == 3 and Score_p2 < 3:
        #IF player 1 won
        winner = clientconn[0]
        #send to player 1 client
        winner.send(f"Congratulations, You won!".encode(FORMAT))
        winner.close()

        #then Player 2 lost
        loser = clientconn[1]
        loser.send("Sorry, try again next time!".encode(FORMAT))
        loser.close()
    else:
        #Else,  Player 2 won
        winner = clientconn[1]
        winner.send(f"Congratulations, You won!".encode(FORMAT))
        print("SENTTT2")
        winner.close()
        # Player 1 lost
        loser = clientconn[0]
        loser.send("Sorry, try again next time!".encode(FORMAT))
        print("Sorry2")
        loser.close()

#Game function
def game():
    #global scoreing variables
    global Score_p1, Score_p2

    # SERIES OF CONDITIONALS TO CHECK FOR EACH INPUT BY BOTH PLAYERS(CLIENTS)
    if inputs[0] == "R" and inputs[1] == "R":
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        print("ITS A DRAW, NO POINTS GIVEN")
        #Shouldve been sent to the client, but due to very late time/submission already
        # I will be skipping this one.
        # Since There is still debugging to be done since my server send 3 messages to client
        # but in my client file, it accepts 1 only
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                ITS A DRAW, NO POINTS GIVEN

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))
        #THIS IS where I shouldve been sending the message to the client file.
    elif inputs[0] == "P" and inputs[1] == "R":
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        Score_p1 += 1
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                Player 1  wins the round!

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))
        
        message = f" Scores:   Player 1 is  {Score_p1}  Player 2 is  {Score_p2}"
        print(message)
    elif inputs[0] == "S" and inputs[1] == "R":        
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        Score_p2 += 1
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                Player 2  wins the round!

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))
        
        message = f" Scores:   Player 1 is  {Score_p1}  Player 2 is  {Score_p2}"
        print(message)
    elif inputs[0] == "R" and inputs[1] == "P":        
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        Score_p2 += 1
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                Player 2  wins the round!

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))
        
        message = f" Scores:   Player 1 is  {Score_p1}  Player 2 is  {Score_p2}"
        print(message) 
    elif inputs[0] == "P" and inputs[1] == "P":        
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        print("ITS A DRAW, NO POINTS GIVEN")
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                ITS A DRAW, NO POINTS GIVEN

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))
    elif inputs[0] == "S" and inputs[1] == "P":        
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        Score_p1 += 1
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                Player 1  wins the round!

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))
        
        message = f" Scores:   Player 1 is  {Score_p1}  Player 2 is  {Score_p2}"
        print(message)
    elif inputs[0] == "R" and inputs[1] == "S":        
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        Score_p1 += 1
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                Player 1  wins the round!

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))
        
        message = f" Scores:   Player 1 is  {Score_p1}  Player 2 is  {Score_p2}"
        print(message)
        #conn.send(message).encode(FORMAT)
    elif inputs[0] == "P" and inputs[1] == "S":        
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        Score_p2 += 1
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                Player 2  wins the round!

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))
        
        message = f" Scores:   Player 1 is  {Score_p1}  Player 2 is  {Score_p2}"
        print(message)
    elif inputs[0] == "S" and inputs[1] == "S":        
        print(f"Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} ")  
        print("ITS A DRAW, NO POINTS GIVEN")
        result = f"""
            "Player 1 hand is {inputs[0]} AND Player 2 hand is {inputs[1]} " 
                ITS A DRAW, NO POINTS GIVEN

                Current Score: 
                [Player 1: {Score_p1}] 
                [Player 2: {Score_p2}]
                """
        #clientconn[0].send(result.encode(FORMAT))
        #clientconn[1].send(result.encode(FORMAT))



#HERE IS WHERE IT RUNS
print("[STARTING] Server is starting")
start()