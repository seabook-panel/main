import socket
from urllib.request import urlopen
from json import load

def local_ip():
    hostname = socket.getfqdn(socket.gethostname())
    addr = socket.gethostbyname(hostname)
    return addr


def external_ip():
    try:
        my_ip = load(urlopen('http://httpbin.org/ip'))['origin']
        return my_ip
    except:
        return "获取公网IP失败！"
        # 防止由于测试给API带来太大压力，这里返回错误即可。