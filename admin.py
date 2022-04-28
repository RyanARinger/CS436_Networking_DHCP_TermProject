#!/usr/bin/env python3
import uuid
import socket
from datetime import datetime

# Time operations in python
# timestamp = datetime.fromisoformat(isotimestring)

class Connection:
    def __init__(self, macAddress, ipAddress, timestamp):
        self.macAddress = macAddress
        self.ipAddress = ipAddress
        self.timestamp = timestamp

    def __str__(self):
        return "MAC Address: " + str(self.macAddress) + ", IP Address: " + str(self.ipAddress) + ", timestamp: " + str(self.timestamp)

    def getMessageString(self):
        return str(self.macAddress) + " " + str(self.ipAddress) + " " + str(self.timestamp)

def parse_message(message):
    decodedMessage = message.decode()
    print("Client recieved -> " + decodedMessage)
    parsedMessage = decodedMessage.split(" ")
    return parsedMessage

def processResponse(parsed_message):
    if parsed_message[0] == "OFFER":
        send_Request(parsed_message[1], parsed_message[2], parsed_message[3])
        pass
    elif parsed_message[0] == "ACKNOWLEDGE":
        CONNECTION.ipAddress = parsed_message[2]
        CONNECTION.timestamp = parsed_message[3]
        menu()
        pass
    elif parsed_message[0] == "DECLINE":
        print("No address offered, Allocation declined")
        pass
    else:
        print("Odd message recieved: ")
        for item in parsed_message:
            print(item)

def send_Request(macAddress, ipAddress, timestamp):
    message = "REQUEST " + macAddress + " " + ipAddress + " " + timestamp
    send_Message(message)
    pass

def send_Message(dhcpMessage):
    print("Client sending -> " + dhcpMessage)
    CLIENTSOCKET.sendto(dhcpMessage.encode(), (SERVER_IP, SERVER_PORT))
    pass

def release_Ip():
    message = "RELEASE " + CONNECTION.getMessageString()
    send_Message(message)
    menu()

def renew_Ip():
    send_Message("RENEW " + CONNECTION.getMessageString())
    message, _ = CLIENTSOCKET.recvfrom(4096)
    processResponse(parse_message(message))

def request_List():
    send_Message("LIST")
    message, _ = CLIENTSOCKET.recvfrom(4096)
    print(message.decode())
    menu()

def menu():
    print("IP allocation management options:")
    print("0: LIST (Admin Only)")
    print("1: RELEASE IP")
    print("2: RENEW Ip allocation")
    print("3: Exit management terminal")
    
    

    validOption = False
    while not validOption:
        option = input("Select: ")
        if option == "0":
            validOption = True
            request_List()
        elif option == "1":
            validOption = True
            release_Ip()
        elif option == "2":
            validOption = True
            renew_Ip()
        elif option == "3":
            validOption = True
            quit()
            return
        else:
            print("Make a valid selection from the listed options.")
            pass
    pass
# Extract local MAC address [DO NOT CHANGE]
MAC = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1]).upper()
CONNECTION = Connection(MAC, None, None)
# SERVER IP AND PORT NUMBER [DO NOT CHANGE VAR NAMES]
SERVER_IP = "10.0.0.100"
SERVER_PORT = 9000


CLIENTSOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Sending DISCOVER message
message = "DISCOVER " + MAC
CLIENTSOCKET.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

# LISTENING FOR RESPONSE
while True:
    message, _ = CLIENTSOCKET.recvfrom(4096)

    parsed_message = parse_message(message)

    dhcpAction = processResponse(parsed_message)
    