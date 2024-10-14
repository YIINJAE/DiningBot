from django.core.paginator import Paginator  # 페이징 처리를 위한 Django 모듈 (현재 코드에서 사용되지 않음)
from django.shortcuts import render  # 페이지 렌더링을 위한 Django 모듈
import socket, time  # 소켓 통신 및 시간 지연을 위한 모듈
from _thread import *  # 멀티스레딩을 위한 모듈 (현재 코드에서 사용되지 않음)

# 협동 로봇을 부팅하는 뷰 함수
def cs_poweron(request):
    print("초기협동부팅")  # 로봇 부팅 과정 시작 로그
    
    # 로봇 제어 장치의 IP 주소와 제어 포트 번호
    ip = '192.168.1.20'
    port = 29999  # 로봇의 직접 제어 포트 (29999)

    # 서버의 주소 정보 설정 (IP 주소 또는 호스트 이름 가능)
    HOST = ip
    # 서버에서 사용할 포트 번호 설정
    PORT = port       

    # 소켓 객체 생성 (IPv4, TCP 방식 사용)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 HOST와 PORT를 사용하여 서버에 접속 시도
    ck = client_socket.connect((HOST, PORT))

    # 로봇 제어 명령어 "robotControl -on"을 서버에 전송
    data = "robotControl -on"
    data = data + "\n"  # 명령어에 줄바꿈 추가 (서버가 명령어 구분을 위해 사용)
    print("협동전원 On")  # 로봇 전원이 켜졌음을 로그로 출력

    # 명령어를 서버로 전송
    client_socket.sendall(data.encode())  # 문자열을 바이트 형태로 인코딩하여 전송
    time.sleep(10)  # 10초 동안 대기 (부팅 시간이 필요할 수 있음)

    # 브레이크 해제를 위한 명령어 전송
    data = "brakeRelease" + "\n"
    client_socket.sendall(data.encode())
    print("협동브레이크 off")  # 브레이크 해제 성공 로그 출력

    # 부팅이 완료된 후, 렌더링할 HTML 페이지 반환
    return render(request, './ramen/init_cs_power.html')  # ramen 폴더 내의 HTML 파일 렌더링
