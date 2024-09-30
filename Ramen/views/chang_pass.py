from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from ..models import MyModel

def change_password(request, employee_id, count):
    if request.method == "POST":
        user = request.user
        origin_password = request.POST.get("origin_password")
        print('현재비번:', origin_password)
        
        # 사용자 인증 확인
        if request.user.is_authenticated:
            print(f'로그인된 사용자: {request.user}')
        else:
            print('사용자가 로그인되어 있지 않습니다.')
            messages.error(request, '사용자가 인증되지 않았습니다')
            return render(request, 'common/change_password.html')

        # 비밀번호 확인
        if check_password(origin_password, user.password):
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            print('새비번:', new_password)
            print('새비번확인:', confirm_password)
            
            # 새 비밀번호와 확인 비밀번호가 일치하는지 확인
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                print('비번저장')

                # 로그인 처리
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                # messages.success(request, '비밀번호가 성공적으로 변경되었습니다')

                # 리다이렉션 처리
                my_model_instance = MyModel(
                employee_id=employee_id, 
                name=user.first_name,  # 이름을 User 모델의 first_name 필드에서 가져옵니다.
                count=count
                )
                my_model_instance.save()

                return redirect('Ramen:index05',  employee_id=employee_id, count=count)
            else:
                messages.error(request, '새로운 비밀번호가 일치하지 않습니다')
        else:
            messages.error(request, '현재 비밀번호가 올바르지 않습니다.')
        return render(request, 'common/change_password.html', {'employee_id': employee_id, 'count': count})

    else:
        return render(request, 'common/change_password.html', {'employee_id': employee_id, 'count': count})

