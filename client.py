import socket
import time
import threading
import sys
import select


'''
    GLOBAL CONSTANTS
'''

HEADER = 64
PORT = 5050
SERVER = '192.168.1.112'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'BYE'

# Make the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the client
client.connect(ADDR)

'''
    CLIENT FUNCTIONS
'''

# Function to send message to the client
def sendMsgUtil(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    # Send the length of the message
    client.send(send_length)

    # Send the message 
    client.send(message) 



'''
    UTILITY FUNCTIONS
'''

# Method to print the help function
def help():
    # print("1. ?help for help")
    print("1. BYE for exiting")


def sendMsg(username):
    while True:
        # maintains a list of possible open streams
        sockets_list = [sys.stdin, client]

        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

        for socket in read_sockets:
            if socket == client:
                msg = socket.recv(2048).decode(FORMAT)
                print(msg)
            else:
                msg = input()
                if(msg == DISCONNECT_MESSAGE):
                    sendMsgUtil(DISCONNECT_MESSAGE)
                    sys.stdout.flush()
                    return
                if msg == "" or msg == " ":
                    continue
                sendMsgUtil(msg)
                print(f"YOU > {msg}")
                
    
    client.close()
    
    

'''
    DRIVER CODE
'''

username = input("What is the username? ")
if username: 
    help()
    sendMsgUtil(username)
    sendMsg(username)

else:
    print("No Username Found.")
    print("[Exiting]...")