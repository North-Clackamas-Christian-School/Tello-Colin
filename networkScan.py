# A basic script to scan a local network for IP addresses to indentify Tello EDU drones

# Import modules
import subprocess
import ipaddress
from subprocess import Popen, PIPE
import socket

def badScan():
    # Create the network
    # The IP below is associated with the TP-Link wireless router
    # https://amzn.to/2TR1r56
    ip_net = ipaddress.ip_network(u'10.0.3.1/24', strict=False)

    # Loop through the connected hosts
    for ip in ip_net.hosts():

        # Convert the ip to a string so it can be used in the ping method
        ip = str(ip)
        
        # Let's ping the IP to see if it's online
        toping = Popen(['command', '-c', '1', '-W', '50', ip], stdout=PIPE)
        output = toping.communicate()[0]
        hostalive = toping.returncode
        
        # Print whether or not device is online
        if hostalive ==0:
            print(ip, "is online")
        else:
            print(ip, "is offline")

def NewScan():
    # Tello address
    tello_address = ('192.168.10.1', 8889)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 61031))

    # Command to send
    message = "command"

    # Send the command
    sock.sendto(message.encode('utf-8'), tello_address)
    print('message sent')
    # Receive the response (optional)

    response, ip_address = sock.recvfrom(1024)
    print(f"Received message: {response.decode(encoding='utf-8')}")
    sock.close()

NewScan()