from django.shortcuts import render, redirect  # 템플릿 렌더링과 리디렉션을 위한 모듈
from django.contrib.auth import authenticate, login  # 사용자 인증 및 로그인 처리를 위한 모듈
from django.contrib import messages  # Django 메시지 프레임워크 사용
from ..models import MyModel, OrderStatus  # MyModel과 OrderStatus 모델 임포트
from django.contrib.messages import get_messages  # Django 메시지에서 메시지 처리
from datetime import datetime  # 현재 시간 처리를 위한 모듈
import logging  # 로그 기록을 위한 모듈

# 로그인 뷰 함수
def login_view(request):
    # POST 요청일 경우 (로그인 시도)
    if request.method == 'POST':
        # POST 요청에서 사번과 비밀번호 가져오기
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        count = request.POST.get('count')  # 주문 수량 count 값도 함께 받음

        # count 값이 빈 문자열이거나 잘못된 값일 경우 0으로 설정
        try:
            count = int(count)
        except (TypeError, ValueError):
            count = 0

        # 입력된 사번과 비밀번호로 사용자 인증
        user = authenticate(request, username=employee_id, password=password)

        # 인증에 성공했을 경우 (유효한 사용자라면)
        if user is not None:
            # 사용자가 처음 로그인하는지 확인 (last_login 값이 None이면 처음 로그인)
            if user.last_login is None:
                # 사용자가 처음 로그인하면 비밀번호 변경 페이지로 리디렉션 (비밀번호 변경이 필요하다고 가정)
                login(request, user)  # 먼저 로그인 처리
                # 비밀번호 변경 페이지로 이동, employee_id와 count 값을 넘겨줌
                return redirect('Ramen:pass', employee_id=employee_id, count=count)

            # 사용자가 처음이 아닌 경우 정상적으로 로그인 처리
            login(request, user)

            # MyModel에 원본 주문 데이터 저장 (로그 기록 용도)
            my_model_instance = MyModel(
                date=datetime.now().replace(microsecond=0),  # 초 단위까지만 저장
                employee_id=employee_id,  # 사번 저장
                name=user.first_name,  # User 모델에서 이름 가져와서 저장
                count=count  # 주문 수량 저장
            )
            my_model_instance.save()

            # OrderStatus에 주문 상태 데이터 저장 (주문 상태 모델에 추가)
            order_status_instance = OrderStatus.objects.create(
                employee_id=employee_id,  # 사번 저장
                name=user.first_name,  # 이름 저장
                initial_count=count,  # 초기 주문 수량 저장
                remaining_count=count  # 남은 주문 수량 저장 (초기값은 주문 수량과 동일)
            )

            # 로그 기록 (사용자 정보 및 주문 수량 기록)
            logger = logging.getLogger('my_custom_logger')
            logger.info('사번: %s, 이름: %s, 주문수량: %d', employee_id, user.first_name, count)

            # 로그인 후 사번과 count 값을 사용하여 index05 페이지로 리디렉션
            return redirect('Ramen:index05', count=count, employee_id=employee_id)

        else:
            # 로그인 실패 시 오류 메시지 출력 및 로그인 페이지 다시 렌더링
            messages.error(request, '사번 또는 비밀번호 확인하세요!!')
            return render(request, 'ramen/db_index00.html', {
                'count': count,  # count 값을 유지하여 반환
                'employee_id': employee_id  # 입력된 사번도 유지하여 반환
            })

    # GET 요청일 경우 (로그인 페이지 접근)
    count = request.GET.get('count', 0)  # URL 파라미터에서 count 값을 가져옴, 없으면 0

    # 메시지 스토리지에서 메시지를 소비하여 삭제
    storage = get_messages(request)
    for message in storage:
        pass  # 메시지 삭제

    # GET 요청 시에도 count 값을 넘겨 로그인 페이지 렌더링
    return render(request, 'ramen/db_index00.html', {'count': count})
