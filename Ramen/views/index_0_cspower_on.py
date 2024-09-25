from django.core.paginator import Paginator
from django.shortcuts import render
import socket, time
from _thread import *


def cs_poweron(request):
    print("초기협동부팅")
    ip='192.168.1.20'
    port=29999  #29999 직접 제어

    # 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
    HOST = ip 
    # 서버에서 지정해 놓은 포트 번호입니다. 
    PORT = port       

    # 소켓 객체를 생성합니다. 
    # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
    ck=client_socket.connect((HOST, PORT))

    data="robotControl -on"
    data=data+"\n"
    print("협동전원 On")

    client_socket.sendall(data.encode())
    time.sleep(10)
    data="brakeRelease"+"\n"
    client_socket.sendall(data.encode())
    print("협동브레이크 off")


    return render(request, './ramen/init_cs_power.html')