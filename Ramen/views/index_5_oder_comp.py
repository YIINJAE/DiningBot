from django.shortcuts import render
from pyModbusTCP.client import ModbusClient
from django.contrib import messages

plc_ip = "192.168.20.100"
mainPlc = ModbusClient(host=plc_ip, unit_id=1, auto_open=True, auto_close=True)

def manual_oder_complete(request, count, employee_id):
    plc_oder_count = int(count)
    # print("라면 주문수량 :", plc_oder_count)
    
    # PLC 명령 전송
    mainPlc.write_multiple_registers(5010, [40])
    mainPlc.write_multiple_registers(5000, [plc_oder_count])
    
    # count와 employee_id 값을 템플릿으로 전달
    return render(request, './ramen/new_index05.html', {'count': count, 'employee_id': employee_id})
