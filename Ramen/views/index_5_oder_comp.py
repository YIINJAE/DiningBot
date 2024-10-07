from django.shortcuts import render
from pyModbusTCP.client import ModbusClient
from django.contrib import messages
import logging

# PLC IP 설정
plc_ip = "192.168.20.100"

def manual_oder_complete(request, count, employee_id):
    plc_oder_count = int(count)

    # ModbusClient 인스턴스 생성 (함수 내부에서 생성하여 안전한 사용 보장)
    mainPlc = ModbusClient(host=plc_ip, unit_id=1, auto_open=True, auto_close=True)
    
    try:
        # PLC 명령 전송
        if mainPlc.open():  # PLC 연결을 확인
            mainPlc.write_multiple_registers(5010, [40])
            mainPlc.write_multiple_registers(5000, [plc_oder_count])
            logging.info(f'PLC에 주문 수량 {plc_oder_count} 전송 성공 - 사번: {employee_id}')
        else:
            logging.error('PLC 연결 실패')
            messages.error(request, 'PLC에 연결할 수 없습니다. 관리자에게 문의하세요.')
            return render(request, './ramen/new_index05.html', {'count': count, 'employee_id': employee_id, 'error': 'PLC 연결 실패'})

    except Exception as e:
        logging.error(f'PLC 명령 전송 중 오류 발생: {str(e)}')
        messages.error(request, 'PLC에 데이터를 전송하는 중 오류가 발생했습니다. 관리자에게 문의하세요.')
        return render(request, './ramen/new_index05.html', {'count': count, 'employee_id': employee_id, 'error': 'PLC 명령 전송 오류'})

    # count와 employee_id 값을 템플릿으로 전달
    return render(request, './ramen/new_index05.html', {'count': count, 'employee_id': employee_id})
