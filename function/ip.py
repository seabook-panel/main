import socket
from urllib.request import urlopen
from json import load

def local_ip():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def external_ip():
    try:
        my_ip = load(urlopen('http://httpbin.org/ip'))['origin']
        return my_ip
    except:
        return None