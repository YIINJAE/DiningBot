import threading
import time
from pyModbusTCP.client import ModbusClient
import logging
from Ramen.models import OrderStatus  # 모델을 임포트

# Modbus 설정
plc_ip = "192.168.20.100"
modbus_client = ModbusClient(host=plc_ip, unit_id=1, auto_open=True, auto_close=True)

# 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 콘솔에 로그 출력
        logging.FileHandler('logs/modbus.log')  # 로그 파일에 기록
    ]
)

def read_modbus_data():
    while True:
        # Modbus 레지스터에서 값 읽기
        registers = modbus_client.read_holding_registers(5020, 1)
        logging.info(f"Received Modbus data: {registers}")

        if registers and registers[0] == 1:  # 읽은 값이 1인 경우
            logging.info("Modbus data is 1, decrementing remaining_count...")

            # remaining_count 값을 감소시키는 로직
            decrement_remaining_count()

        time.sleep(1000000)  # 5초마다 데이터를 읽음

def decrement_remaining_count():
    # remaining_count가 0이 아닌 주문들을 id 오름차순으로 정렬하여 가져옵니다
    orders = OrderStatus.objects.filter(remaining_count__gt=0).order_by('id')

    # 가장 위의 주문의 remaining_count 값을 1 감소시킵니다
    if orders.exists():
        order = orders.first()  # id가 가장 작은 첫 번째 주문
        order.remaining_count -= 1  # remaining_count 값을 1 감소
        order.save()  # 변경 사항 저장
        logging.info(f"Updated order {order.employee_id}: remaining_count = {order.remaining_count}")
    else:
        logging.info("No orders with remaining_count greater than 0.")

def start_modbus_thread():
    logging.info("Starting Modbus communication thread...")
    modbus_thread = threading.Thread(target=read_modbus_data)
    modbus_thread.daemon = True  # 서버가 종료될 때 스레드도 종료되도록 설정
    modbus_thread.start()
    logging.info("Modbus thread started successfully.")

