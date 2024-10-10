import threading  # 멀티스레딩을 위한 모듈
import time  # 시간 관련 함수 제공
from pyModbusTCP.client import ModbusClient  # Modbus 통신을 위한 라이브러리
import logging  # 로깅 설정을 위한 모듈
from Ramen.models import OrderStatus  # Django 모델 임포트
from django.db import transaction  # 데이터베이스 트랜잭션 관리

# Modbus 설정 (PLC의 IP와 기본 통신 설정)
plc_ip = "192.168.20.100"
modbus_client = ModbusClient(host=plc_ip, unit_id=1, auto_open=True, auto_close=True)

# 로깅 설정 (로그를 콘솔과 파일에 남기도록 설정)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 콘솔에 로그 출력
        logging.FileHandler('logs/modbus.log')  # 로그 파일에 기록
    ]
)

# Modbus 데이터를 읽는 함수
def read_modbus_data():
    while True:
        # Modbus 레지스터(5020)에서 값 읽기
        registers = modbus_client.read_holding_registers(5020, 1)

        # 읽은 값이 1인 경우 로직 실행
        if registers and registers[0] == 1:
            logging.info("Modbus data is 1, decrementing remaining_count...")

            # remaining_count를 감소시키는 함수 호출
            decrement_remaining_count()

            # 작업 후 Modbus 레지스터의 값을 0으로 리셋
            success = modbus_client.write_single_register(5020, 0)
            if success:
                logging.info("Modbus register 5020 reset to 0.")
            else:
                logging.error("Failed to reset Modbus register 5020 to 0.")

        # 1초마다 Modbus 데이터를 읽음
        time.sleep(1)

# 주문의 remaining_count를 감소시키는 함수
def decrement_remaining_count():
    # remaining_count가 0이 아닌 주문을 id 오름차순으로 가져옴
    orders = OrderStatus.objects.filter(remaining_count__gt=0).order_by('id')

    # 남은 주문이 있을 경우
    if orders.exists():
        # 가장 첫 번째 주문(remaining_count가 가장 오래된)을 선택
        order = orders.first()
        order.remaining_count -= 1  # remaining_count 1 감소

        # remaining_count가 0 이하가 되면 상태를 COMPLETED로 변경
        if order.remaining_count <= 0:
            order.remaining_count = 0  # 음수로 떨어지지 않게 유지
            order.save()  # 변경 사항 저장
            logging.info(f"Order {order.employee_id} will be marked as COMPLETED in 60 seconds.")
            
            # 타이머가 실행 중이 아닌 경우 타이머를 시작 (60초 후 주문을 완료 상태로 변경)
            if not hasattr(order, 'completion_timer') or not order.completion_timer.is_alive():
                order.completion_timer = threading.Timer(10, mark_order_completed, [order.id])
                order.completion_timer.start()
                logging.info(f"Started timer for order {order.employee_id}.")
        else:
            # remaining_count가 감소된 상태를 저장
            order.save()
            logging.info(f"Updated order {order.employee_id}: remaining_count = {order.remaining_count}")
    else:
        # 남은 주문이 없는 경우 로그 기록
        logging.info("No orders with remaining_count greater than 0.")

# 주문을 COMPLETED 상태로 변경하는 함수
@transaction.atomic
def mark_order_completed(order_id):
    """주문 상태를 COMPLETED로 변경하는 함수"""
    try:
        # 트랜잭션 내에서 안전하게 주문을 가져옴 (락을 사용)
        order = OrderStatus.objects.select_for_update().get(id=order_id)
        # remaining_count가 0인 경우에만 상태를 COMPLETED로 변경
        if order.remaining_count == 0:
            order.status = 'COMPLETED'
            order.save()
            logging.info(f"Order {order.employee_id} is now COMPLETED after 60 seconds.")
    except OrderStatus.DoesNotExist:
        # 주문을 찾지 못했을 경우 로그에 에러 기록
        logging.error(f"Order with id {order_id} does not exist.")

# Modbus 통신을 시작하는 함수 (스레드를 이용해 비동기 처리)
def start_modbus_thread():
    logging.info("Starting Modbus communication thread...")
    modbus_thread = threading.Thread(target=read_modbus_data)  # Modbus 데이터를 읽는 스레드 생성
    modbus_thread.daemon = True  # 메인 스레드가 종료되면 함께 종료되도록 설정
    modbus_thread.start()  # 스레드 시작
    logging.info("Modbus thread started successfully.")