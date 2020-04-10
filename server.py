import socket
import threading

'''
    GLOBAL CONSTANTS
'''

HEADER = 64
PORT = 5050
SERVER = '192.168.1.112'
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = 'BYE'


# Create the actual server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket options
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the server to the [ADDR] (bind takes in a tuple as an argument)
server.bind(ADDR)


'''
    SERVER FUNCTIONS
'''

# Store allthe clients
clients_list = []
 
# Function to print the active connections at a time
def clientsConnected():
    print(f"[ACTIVE CONNECTIONS] {len(clients_list)}")

# Function to remove a connection from the server
def remove(connection): 
    if connection in clients_list: 
        clients_list.remove(connection) 

# Function to send mesasges to all the clients
def broadcast(msg, sourceConnection, username):
    msg = f"{username} > " + msg
    msg = msg.encode(FORMAT)
    for client in clients_list :
        if client != sourceConnection:
            try:
                client.send(msg)
            except:
                # Bad connection. Purge it
                client.close()
                remove(client) #  remove the client from the list


# Function to handle the clients as soon as they arrive
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} joined the server.")
    
    # Receive username of the client
    username_length = int(conn.recv(HEADER).decode(FORMAT))
    username = conn.recv(username_length).decode(FORMAT)

    connected=True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if(msg == DISCONNECT_MESSAGE):
                msg = "[DISCONNECTING]"
                print(f"{msg} {username}")
                # remove(conn) # Remove the client from the client_list
                # clientsConnected()
                connected=False
                break

            print(f"[{addr}] {msg}")
            if(msg == DISCONNECT_MESSAGE):
                break
            broadcast(msg, conn, username)  # broadcast messages to all the clients


    # Close connection when not connected
    conn.close()
    remove(conn) # purfge the closed connection
    clientsConnected()



# FUNCTION TO START LISTENING FOR REQUESTS
def start():
    server.listen(100)
    print(f"[LISTENING] Server is listening on ip {SERVER}")

    # Listen for requests indefinetely
    while True:        
        conn, addr = server.accept()  # Receive a connection and its address
        clients_list.append(conn) # Add connection to the list
        thread = threading.Thread(target=handle_client, args=(conn,addr))  # Every client runs on a separate thread
        thread.start()
        clientsConnected()

'''
    DRIVER CODE
'''


print(f"[STARTING] Server is starting...")
start()