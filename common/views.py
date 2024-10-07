from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password #BUG : import 확인
from django.contrib import messages, auth


def page_not_found(request, exception):
    return render(request, 'common/404.html', {})




def change_password(request):
    if request.method == "POST":
        user = request.user
        print(f'로그인된 사용자: {user}')  # 현재 로그인된 사용자 확인

        origin_password = request.POST["origin_password"]
        print(f'입력된 현재 비밀번호: {origin_password}')  # 입력된 현재 비밀번호 출력

        # 현재 비밀번호가 맞는지 확인
        if check_password(origin_password, user.password):
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]

            print(f'새 비밀번호: {new_password}')  # 새로 입력된 비밀번호 출력
            print(f'새 비밀번호 확인: {confirm_password}')  # 새 비밀번호 확인 출력

            # 새 비밀번호와 새 비밀번호 확인이 일치하는지 확인
            if new_password == confirm_password:
                # 비밀번호 변경 및 저장
                user.set_password(new_password)
                user.save()
                print(f'비밀번호가 성공적으로 변경되었습니다: {user.password}')  # 변경된 비밀번호 해시 출력

                # 비밀번호 변경 후 로그인 처리
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                print('사용자가 새 비밀번호로 다시 로그인되었습니다.')

                return redirect('profile')  # 프로필 페이지로 리다이렉션
            else:
                print('새 비밀번호와 확인 비밀번호가 일치하지 않습니다.')
                messages.error(request, 'Password not same')
        else:
            print('현재 비밀번호가 일치하지 않습니다.')
            messages.error(request, 'Password not correct')
        
        # 비밀번호 변경 실패 시 변경 페이지 다시 렌더링
        return render(request, 'common/change_password.html')
    else:
        print('GET 요청이 발생했습니다. 비밀번호 변경 페이지를 표시합니다.')
        return render(request, 'common/change_password.html')
