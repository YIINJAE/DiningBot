import threading
import time
from pyModbusTCP.client import ModbusClient
import logging
from Ramen.models import OrderStatus  # 모델을 임포트
from django.db import transaction

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
        # logging.info(f"Received Modbus data: {registers}")

        if registers and registers[0] == 1:  # 읽은 값이 1인 경우
            logging.info("Modbus data is 1, decrementing remaining_count...")

            # remaining_count 값을 감소시키는 로직
            decrement_remaining_count()

            # 작업 후 레지스터 값을 0으로 변경
            success = modbus_client.write_single_register(5020, 0)
            if success:
                logging.info("Modbus register 5020 reset to 0.")
            else:
                logging.error("Failed to reset Modbus register 5020 to 0.")

        time.sleep(1)  # 5초마다 데이터를 읽음

# 주문의 remaining_count를 감소시키고 타이머를 설정하는 함수
def decrement_remaining_count():
    # remaining_count가 0이 아닌 주문들을 id 오름차순으로 정렬하여 가져옵니다
    orders = OrderStatus.objects.filter(remaining_count__gt=0).order_by('id')

    # 가장 위의 주문의 remaining_count 값을 1 감소시킵니다
    if orders.exists():
        order = orders.first()  # id가 가장 작은 첫 번째 주문
        order.remaining_count -= 1  # remaining_count 값을 1 감소

        # remaining_count가 0이 되면 상태를 COMPLETED로 변경하기 전에 60초 타이머 설정
        if order.remaining_count <= 0:
            order.remaining_count = 0  # 0 이하로 떨어지지 않게 유지
            order.save()  # remaining_count가 0인 상태 저장
            logging.info(f"Order {order.employee_id} will be marked as COMPLETED in 60 seconds.")
            
            # 타이머가 이미 설정되지 않은 경우에만 타이머 시작
            if not hasattr(order, 'completion_timer') or not order.completion_timer.is_alive():
                order.completion_timer = threading.Timer(10, mark_order_completed, [order.id])
                order.completion_timer.start()
                logging.info(f"Started timer for order {order.employee_id}.")
        else:
            order.save()  # 감소된 상태를 저장
            logging.info(f"Updated order {order.employee_id}: remaining_count = {order.remaining_count}")
    else:
        logging.info("No orders with remaining_count greater than 0.")

@transaction.atomic
def mark_order_completed(order_id):
    """주문 상태를 COMPLETED로 변경하는 함수"""
    try:
        order = OrderStatus.objects.select_for_update().get(id=order_id)  # 락을 사용해 데이터를 안전하게 가져옴
        if order.remaining_count == 0:  # remaining_count가 0일 때만 COMPLETED 상태로 변경
            order.status = 'COMPLETED'
            order.save()
            logging.info(f"Order {order.employee_id} is now COMPLETED after 60 seconds.")
    except OrderStatus.DoesNotExist:
        logging.error(f"Order with id {order_id} does not exist.")


# def decrement_remaining_count():
#     # remaining_count가 0이 아닌 주문들을 id 오름차순으로 정렬하여 가져옵니다
#     orders = OrderStatus.objects.filter(remaining_count__gt=0).order_by('id')

#     # 가장 위의 주문의 remaining_count 값을 1 감소시킵니다
#     if orders.exists():
#         order = orders.first()  # id가 가장 작은 첫 번째 주문
#         order.remaining_count -= 1  # remaining_count 값을 1 감소

#         # remaining_count가 0이 되면 상태를 COMPLETED로 변경
#         if order.remaining_count <= 0:
#             order.remaining_count = 0  # 0 이하로 떨어지지 않게 유지
#             order.status = 'COMPLETED'  # 상태를 COMPLETED로 변경
#             logging.info(f"Order {order.employee_id} is now COMPLETED.")

#         order.save()  # 변경 사항 저장
#         logging.info(f"Updated order {order.employee_id}: remaining_count = {order.remaining_count}")
#     else:
#         logging.info("No orders with remaining_count greater than 0.")

def start_modbus_thread():
    logging.info("Starting Modbus communication thread...")
    modbus_thread = threading.Thread(target=read_modbus_data)
    modbus_thread.daemon = True  # 서버가 종료될 때 스레드도 종료되도록 설정
    modbus_thread.start()
    logging.info("Modbus thread started successfully.")

