from django.shortcuts import render
from pyModbusTCP.client import ModbusClient  # Modbus TCP 통신을 위한 모듈
from django.contrib import messages  # 사용자에게 메시지를 전달하는 기능
import logging  # 로그 기록을 남기기 위한 모듈
import time
# PLC의 IP 주소를 설정
plc_ip = "192.168.20.100" # test ip
# plc_ip = "192.168.20.100" # DiningBot plc ip

# 주문 완료를 수동으로 처리하는 뷰
def manual_oder_complete(request, count, employee_id):
    plc_oder_count = int(count)  # 전달받은 주문 수량을 정수로 변환

    # ModbusClient 인스턴스 생성 (이 함수 내에서 생성하여 사용 범위를 제한)
    # PLC에 접속할 때 IP 주소와 유닛 ID를 사용
    mainPlc = ModbusClient(host=plc_ip, unit_id=1, auto_open=True, auto_close=True)
    
    try:
        # PLC 명령 전송 시작
        if mainPlc.open():  # PLC 연결이 성공적으로 이루어졌는지 확인
            # 24.10.21 PLC 주문시에 카운터 쓰고 동작허가 40 출력 변경 YI.INJAE
            # PLC에 주문 수량을 5000번 레지스터에 기록
            mainPlc.write_multiple_registers(5000, [plc_oder_count])
            time.sleep(0.5)
            # PLC에 레지스터 값을 기록 (40을 5010번 레지스터에 기록)
            mainPlc.write_multiple_registers(5010, [40])

            # 로그에 성공 메시지를 기록 (사번과 주문 수량 포함)
            logging.info(f'PLC에 주문 수량 {plc_oder_count} 전송 성공 - 사번: {employee_id}')
        else:
            # PLC 연결에 실패한 경우 처리
            logging.error('PLC 연결 실패')  # 오류 로그 기록
            messages.error(request, 'PLC에 연결할 수 없습니다. 관리자에게 문의하세요.')  # 사용자에게 오류 메시지 전달
            # 오류가 발생했을 때 템플릿을 렌더링하고 사용자에게 오류 정보 전달
            return render(request, './ramen/new_index05.html', {'count': count, 'employee_id': employee_id, 'error': 'PLC 연결 실패'})

    except Exception as e:
        # PLC 명령 전송 중 예외가 발생한 경우 처리
        logging.error(f'PLC 명령 전송 중 오류 발생: {str(e)}')  # 예외에 대한 오류 로그 기록
        messages.error(request, 'PLC에 데이터를 전송하는 중 오류가 발생했습니다. 관리자에게 문의하세요.')  # 사용자에게 오류 메시지 전달
        # 예외 발생 시 템플릿을 렌더링하고 사용자에게 오류 정보 전달
        return render(request, './ramen/new_index05.html', {'count': count, 'employee_id': employee_id, 'error': 'PLC 명령 전송 오류'})

    # 주문 완료 처리가 성공적으로 끝나면, count와 employee_id 값을 템플릿으로 전달하여 렌더링
    return render(request, './ramen/new_index05.html', {'count': count, 'employee_id': employee_id})
