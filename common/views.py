from django.contrib.auth import authenticate, login  # 사용자 인증 및 로그인 관련 함수
from django.shortcuts import render, redirect  # 템플릿 렌더링 및 리다이렉트 처리
from django.contrib.auth.hashers import check_password  # 비밀번호 검증을 위한 함수
from django.contrib import messages, auth  # 메시지 표시 및 사용자 인증 관련 모듈

# 404 페이지가 발생했을 때 렌더링할 뷰 함수
def page_not_found(request, exception):
    # 404 에러가 발생하면 'common/404.html' 템플릿을 렌더링
    return render(request, 'common/404.html', {})

# 비밀번호 변경 뷰
def change_password(request):
    # POST 요청이 왔을 때 (비밀번호 변경 요청)
    if request.method == "POST":
        # 현재 로그인된 사용자 객체
        user = request.user
        print(f'로그인된 사용자: {user}')  # 현재 로그인된 사용자 출력 (디버깅용)

        # 입력된 현재 비밀번호를 가져옴
        origin_password = request.POST["origin_password"]
        print(f'입력된 현재 비밀번호: {origin_password}')  # 입력된 현재 비밀번호 출력 (디버깅용)

        # 현재 비밀번호가 맞는지 확인
        if check_password(origin_password, user.password):
            # 새 비밀번호 및 확인용 비밀번호를 가져옴
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]

            # 새로 입력된 비밀번호와 확인용 비밀번호 출력 (디버깅용)
            print(f'새 비밀번호: {new_password}')  
            print(f'새 비밀번호 확인: {confirm_password}')

            # 새 비밀번호와 새 비밀번호 확인이 일치하는지 확인
            if new_password == confirm_password:
                # 비밀번호를 새 비밀번호로 변경하고 저장
                user.set_password(new_password)
                user.save()
                print(f'비밀번호가 성공적으로 변경되었습니다: {user.password}')  # 변경된 비밀번호 해시 출력 (디버깅용)

                # 비밀번호 변경 후 사용자 다시 로그인 처리
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                print('사용자가 새 비밀번호로 다시 로그인되었습니다.')  # 디버깅 메시지 출력

                # 비밀번호 변경이 완료되면 'profile' 페이지로 리다이렉트
                return redirect('profile')
            else:
                # 새 비밀번호와 확인 비밀번호가 일치하지 않으면 에러 메시지 출력
                print('새 비밀번호와 확인 비밀번호가 일치하지 않습니다.')  # 디버깅 메시지 출력
                messages.error(request, 'Password not same')  # 사용자에게 오류 메시지 전달
        else:
            # 현재 비밀번호가 맞지 않으면 에러 메시지 출력
            print('현재 비밀번호가 일치하지 않습니다.')  # 디버깅 메시지 출력
            messages.error(request, 'Password not correct')  # 사용자에게 오류 메시지 전달
        
        # 비밀번호 변경 실패 시 다시 비밀번호 변경 페이지를 렌더링
        return render(request, 'common/change_password.html')
    else:
        # GET 요청이 발생하면 비밀번호 변경 페이지를 보여줌
        print('GET 요청이 발생했습니다. 비밀번호 변경 페이지를 표시합니다.')  # 디버깅 메시지 출력
        return render(request, 'common/change_password.html')
