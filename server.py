#!/usr/bin/env python3
import socket
from ipaddress import IPv4Interface
from datetime import datetime, timedelta

# Time operations in python
# isotimestring = datetime.now().isoformat()
# timestamp = datetime.fromisoformat(isotimestring)
# 60secfromnow = timestamp + timedelta(seconds=60)

#ips
class IpInformation:
    def __init__(self, address, client, reserved, expiration):
        self.address = address #ip address
        self.client = client #client MAC (or IP; TBD)
        self.reserved = reserved #boolean
        self.expiration = expiration #expiration ISO

#records
class Record:
    def __init__(self, recordNumber, mAC, iP, timestamp, acked, active):
        self.recordNumber = recordNumber
        self.macAddress = mAC
        self.ipAddress = iP
        self.timestamp = timestamp
        self.acknowledged = acked
        self.active = active

# Choose a data structure to store your records
availableIps = list()
records = list()
globalRecordCounter = 0

# List containing all available IP addresses as strings
ip_addresses = [ip.exploded for ip in IPv4Interface("192.168.45.0/28").network.hosts()]

for ip in ip_addresses:
    #initially, and whenever an ip is not in use there will be no connected client
    #or expiration timestamp
    availableIps.append(IpInformation(ip, "", False, ""))


# Parse the client messages
def parse_message(message):
    decodedMessage = message.decode()

    print(decodedMessage)

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
        print("Found DISCOVER Message")
        message = offer_Ip(parsed_message[1])
        print("1" + message)
        pass
    elif parsed_message[0] == "REQUEST":
        #send ACK
        #update ip information object
        #False -> True
        pass
    elif parsed_message[0] == "RELEASE":
        # search in list for matching recieved IP or mac record
        # set reserved to False
        # remove expiration timestamp
        pass
    elif parsed_message[0] == "RENEW":
        # search in list for matching recieved IP or mac record
        # update record
        # up ip information w/ new timestamp
            # update reserved boolean just in case False -> True
        pass
    else:
        raise Exception("Invalid Request Recieved")


def update_IPInformation(ipAddress, macAddress, reserved, timestamp):
    for ip in availableIps:
        if ip.address == ipAddress:
            print("here in info")
            ip = IpInformation(ipAddress, macAddress, reserved, timestamp)
            print("ipInfo: " + ip)
            break

def update_record(recordNumber, mAC, iP, timestamp, acked, active):
    for record in records:
        if record.recordNumber == recordNumber:
            print("here in record")
            record.macAddress = mAC
            record.ipAddress = ip
            record.timestamp = timestamp
            record.acked = acked
            record.active = active
            break

def offer_Ip(macAddress):
    for ip in availableIps:
        if ip.reserved == False:
            print("here in offer")
            print("offered IP: " + ip.address)
            # currentTime = datetime.datetime.now().isoformat()
            # expirationTime = currentTime + timedelta(0, 60, 0, 0, 0, 0, 0, 0)
            update_IPInformation(ip.address, macAddress, True, None)
            records.append(Record(globalRecordCounter, macAddress, ip.address, None, False, False))
            globalRecordCounter = globalRecordCounter + 1
            return "OFFER " + macAddress + ip.address + datetime.datetime.now().isoformat()
    #return nothing found
        
# Start a UDP server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Avoid TIME_WAIT socket lock [DO NOT REMOVE]
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", 9000))
print("DHCP Server running...")

try:
    while True:
        message, clientAddress = server.recvfrom(4096)
        print(message)
        parsed_message = parse_message(message)
        print(parsed_message)
        response = dhcp_operation(parsed_message)
        print(response)
        server.sendto(response.encode(), clientAddress)
except OSError:
    pass
except KeyboardInterrupt:
    pass
except Exception:
    pass

server.close()
