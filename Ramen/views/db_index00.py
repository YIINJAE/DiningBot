from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from ..models import MyModel, OrderStatus  # OrderStatus 모델을 가져옵니다.
from django.contrib.messages import get_messages
from datetime import datetime
import logging

def login_view(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        count = request.POST.get('count')  # POST 요청에서 count 값을 받음

        # count 값이 빈 문자열일 경우 처리
        try:
            count = int(count)
        except (TypeError, ValueError):
            count = 0

        # 사번과 비밀번호로 사용자 인증
        user = authenticate(request, username=employee_id, password=password)

        # 인증된 사용자라면
        if user is not None:
            # 사용자가 처음 로그인하는지 확인 (last_login이 None인 경우 처음 로그인)
            if user.last_login is None:
                # 먼저 로그인 처리 후 비밀번호 변경 페이지로 리디렉션
                login(request, user)  # 로그인 처리
                return redirect('Ramen:pass', employee_id=employee_id, count=count)  # 비밀번호 변경 페이지로 리디렉션

            # 로그인 처리
            login(request, user)

            # MyModel에 주문 데이터 저장 (원본 데이터)
            my_model_instance = MyModel(
                date=datetime.now().replace(microsecond=0),
                employee_id=employee_id, 
                name=user.first_name,  # 이름을 User 모델의 first_name 필드에서 가져옵니다.
                count=count
            )
            my_model_instance.save()

            # OrderStatus에 주문 상태 데이터 저장
            order_status_instance = OrderStatus.objects.create(
                employee_id=employee_id,
                name=user.first_name,
                initial_count=count,
                remaining_count=count
            )

            # 로그 출력
            logger = logging.getLogger('my_custom_logger')
            logger.info('사번: %s, 이름: %s, 주문수량: %d', employee_id, user.first_name, count)

            # 사번과 count 값을 index05로 넘김
            return redirect('Ramen:index05', count=count, employee_id=employee_id)  # 로그인 성공 시 index05로 리디렉션

        else:
            messages.error(request, '사번 또는 비밀번호 확인하세요!!')
            # 로그인 실패 시에도 count 값을 유지하며 다시 로그인 페이지를 렌더링
            return render(request, 'ramen/db_index00.html', {
                'count': count,
                'employee_id': employee_id
            })

    # GET 요청 시에도 count 값을 유지하도록 처리
    count = request.GET.get('count', 0)

    storage = get_messages(request)
    for message in storage:
        pass  # 메시지를 소비하여 삭제

    return render(request, 'ramen/db_index00.html', {'count': count})