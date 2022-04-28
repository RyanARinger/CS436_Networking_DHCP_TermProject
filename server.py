#!/usr/bin/env python3
import socket
from ipaddress import IPv4Interface
from datetime import datetime, timedelta

# Time operations in python
# isotimestring = datetime.now().isoformat()
# timestamp = datetime.fromisoformat(isotimestring)
# 60secfromnow = timestamp + timedelta(seconds=60)

#ips

    

#records
class Record:
    def __init__(self, recordNumber, mAC, iP, timestamp, acked):
        self.recordNumber = recordNumber
        self.macAddress = mAC
        self.ipAddress = iP
        self.timestamp = timestamp
        self.acknowledged = acked
    def __str__(self):
        return "[Record NO. " + str(self.recordNumber) + "], IP Address: " + str(self.ipAddress) + ", MAC Address: " + str(self.macAddress) + ", Acked: " + str(self.acknowledged) + ", Expiration: " + str(self.timestamp) + "\n"

# Choose a data structure to store your records
records = []


# List containing all available IP addresses as strings
ip_addresses = [ip.exploded for ip in IPv4Interface("192.168.45.0/28").network.hosts()]

recordCount = 0
for ip in ip_addresses:
    #initially, and whenever an ip is not in use there will be no connected client
    #or expiration timestamp
    records.append(Record(recordCount, "", ip, "", False))
    recordCount = recordCount + 1


# Parse the client messages
def parse_message(message):
    decodedMessage = message.decode()
    print("Server recieved -> " + decodedMessage)
    parsedMessage = decodedMessage.split(" ")
    return parsedMessage


# Calculate response based on message
def dhcp_operation(parsed_message):
    if parsed_message[0] == "LIST":
        #get records 
        #send LIST
        pass
    elif parsed_message[0] == "DISCOVER":
        #check for next available IP
        #send OFFER
        return offer_Ip(parsed_message[1])
    elif parsed_message[0] == "REQUEST":
        #send ACK
        #update ip information object
        #False -> True
        return acknowledge_Ip(parsed_message[1])
        pass
    elif parsed_message[0] == "RELEASE":
        # search in list for matching recieved IP or mac record
        # set reserved to False
        # remove expiration timestamp
        
        return "got release"
        pass
    elif parsed_message[0] == "RENEW":
        # search in list for matching recieved IP or mac record
        # update record
        # up ip information w/ new timestamp
            # update reserved boolean just in case False -> True
        return "got renew"
        pass
    else:
        print("Invalid Request Recieved: " + parsed_message[0])
        raise Exception("Invalid Request Recieved")


def update_record(ipAddress, macAddress, timestamp, acked):
    for record in records:
        if record.ipAddress == ipAddress:
            record.macAddress = macAddress
            record.ipAddress = ipAddress
            record.timestamp = timestamp
            record.acked = acked
            return

def offer_Ip(macAddress):
    for ip in records:
        if ip.macAddress == macAddress:
            currentTime = datetime.now().isoformat()
            expirationTime = currentTime + str(timedelta(0, 60, 0, 0, 0, 0, 0))
            update_record(ip.ipAddress, macAddress, expirationTime, False)
            responseMessage = "OFFER " + macAddress + " " + ip.ipAddress + " " + expirationTime
            return responseMessage
    for ip in records:
        if ip.macAddress == "" or datetime.fromisoformat(ip.timestamp) < datetime().now():
            currentTime = datetime.now().isoformat()
            expirationTime = currentTime + str(timedelta(0, 60, 0, 0, 0, 0, 0))
            update_record(ip.ipAddress, macAddress, expirationTime, False)
            responseMessage = "OFFER " + macAddress + " " + ip.ipAddress + " " + expirationTime
            return responseMessage
    return None
        
def acknowledge_Ip(macAddress):
    for ip in records:
        if ip.macAddress == macAddress and ip.timestamp < datetime.now().isoformat():
            currentTime = datetime.now().isoformat()
            expirationTime = currentTime + str(timedelta(0, 60, 0, 0, 0, 0, 0))
            update_record(ip.ipAddress, macAddress, expirationTime, True)
            responseMessage = "ACKNOWLEDGE " + macAddress + " " + ip.ipAddress + " " + expirationTime
            return responseMessage

# Start a UDP server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Avoid TIME_WAIT socket lock [DO NOT REMOVE]
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", 9000))
print("DHCP Server running...")

# for record in records:
#     print(record)

try:
    while True:
        message, clientAddress = server.recvfrom(4096)
        parsed_message = parse_message(message)
        response = dhcp_operation(parsed_message)
        print("Server sending -> " + response)
        server.sendto(response.encode(), clientAddress)
        
except OSError:
    print("OSERROR")
    pass
except KeyboardInterrupt:
    print("KEYBOARDINTERRUPT")
    pass
except Exception as e:
    print(e)
    print(traceback.format_exc())
    pass

server.close()
