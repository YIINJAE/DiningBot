from django.contrib.auth.hashers import check_password  # 비밀번호 확인을 위한 함수
from django.contrib import messages  # Django 메시지 프레임워크 사용
from django.contrib.auth import login  # 로그인 처리를 위한 함수
from django.shortcuts import render, redirect  # 템플릿 렌더링 및 리디렉션을 위한 모듈
from ..models import MyModel, OrderStatus  # MyModel과 OrderStatus 모델 임포트

# 비밀번호 변경 뷰 함수
def change_password(request, employee_id, count):
    # POST 요청일 때 (비밀번호 변경 요청)
    if request.method == "POST":
        user = request.user  # 현재 로그인된 사용자 가져오기
        origin_password = request.POST.get("origin_password")  # 입력된 현재 비밀번호 가져오기
        print('현재비번:', origin_password)

        # 사용자 인증 확인 (로그인 여부 체크)
        if request.user.is_authenticated:
            print(f'로그인된 사용자: {request.user}')  # 로그인된 사용자 출력
        else:
            print('사용자가 로그인되어 있지 않습니다.')  # 인증되지 않은 경우 처리
            messages.error(request, '사용자가 인증되지 않았습니다')  # 오류 메시지 표시
            return render(request, 'common/change_password.html')  # 비밀번호 변경 페이지로 리렌더링

        # 현재 비밀번호가 맞는지 확인
        if check_password(origin_password, user.password):
            new_password = request.POST.get("new_password")  # 새 비밀번호 가져오기
            confirm_password = request.POST.get("confirm_password")  # 새 비밀번호 확인 가져오기
            print('새비번:', new_password)
            print('새비번확인:', confirm_password)

            # 새 비밀번호와 확인 비밀번호가 일치하는지 확인
            if new_password == confirm_password:
                user.set_password(new_password)  # 새 비밀번호 설정
                user.save()  # 사용자 저장
                print('비번저장')

                # 비밀번호 변경 후 다시 로그인 처리 (비밀번호 변경 시 세션 만료됨)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                # 주문 정보 저장 (MyModel에 주문 데이터 저장)
                my_model_instance = MyModel(
                    employee_id=employee_id,  # 사번
                    name=user.first_name,  # 사용자 이름 (User 모델에서 가져옴)
                    count=count  # 주문 수량
                )
                my_model_instance.save()  # 주문 정보 저장

                # 주문 상태(OrderStatus) 저장
                order_status_instance = OrderStatus.objects.create(
                    employee_id=employee_id,  # 사번 저장
                    name=user.first_name,  # 이름 저장
                    initial_count=count,  # 초기 주문 수량
                    remaining_count=count  # 남은 주문 수량 (초기에는 주문 수량과 동일)
                )

                # 비밀번호 변경 성공 시 index05로 리디렉션
                return redirect('Ramen:index05', employee_id=employee_id, count=count)

            else:
                # 새 비밀번호와 확인 비밀번호가 일치하지 않는 경우
                messages.error(request, '새로운 비밀번호가 일치하지 않습니다')  # 오류 메시지 표시
        else:
            # 현재 비밀번호가 틀린 경우
            messages.error(request, '현재 비밀번호가 올바르지 않습니다.')  # 오류 메시지 표시

        # POST 요청 실패 시 비밀번호 변경 페이지 다시 렌더링 (오류 메시지와 함께)
        return render(request, 'common/change_password.html', {'employee_id': employee_id, 'count': count})

    # GET 요청일 경우 비밀번호 변경 페이지 렌더링
    else:
        return render(request, 'common/change_password.html', {'employee_id': employee_id, 'count': count})
