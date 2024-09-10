from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from pyModbusTCP.client import ModbusClient
import speech_recognition as sr
import time

plc_ip = "192.168.1.10"
mainPlc = ModbusClient(host=plc_ip, unit_id=1, auto_open=True, auto_close=True)

def voice_oder(request):
    return render(request, './ramen/new_index03.html')

def test_microphone_view(request):
    if request.method == 'POST':
        result = test_microphone()
        if result:
            # 주문이 정상적으로 처리되면 count 값을 가지고 new_index05.html로 리다이렉트
            return JsonResponse({'status': 'redirect', 'url': f'/Ramen/index05/?count={result}'})
        else:
            # 주문 실패 시 index02로 리다이렉트
            return JsonResponse({'status': 'redirect', 'url': '/Ramen/index02/'})
    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'})

def test_microphone(device_index=None):
    recognizer = sr.Recognizer()
    command_map = {
        '한 개': 1, '하나': 1, '한 그릇': 1,
        '두 개': 2, '둘': 2, '두 그릇': 2,
        '세 개': 3, '셋': 3, '세 그릇': 3,
        '네 개': 4, '넷': 4, '네 그릇': 4,
        '다섯 개': 5, '다섯': 5, '다섯 그릇': 5,
        '여섯 개': 6, '여섯': 6, '여섯 그릇': 6,
        '일곱 개': 7, '일곱': 7, '일곱 그릇': 7,
        '여덟 개': 8, '여덟': 8, '여덟 그릇': 8,
        '아홉 개': 9, '아홉': 9, '아홉 그릇': 9,
        # '열 개': 10, '열': 10, '열그릇': 10
    }

    try:
        with sr.Microphone(device_index=device_index) as source:
            recognizer.adjust_for_ambient_noise(source)
            print("주문수량을 말씀해 주세요.")
            print("plz oder")
            audio = recognizer.listen(source)
            time.sleep(2)
            try:
                print("주문 수량 확인중...")
                print("check oder")
                text = recognizer.recognize_google(audio, language="ko-KR")
                # print(f"오더수량: {text}")
                for command, value in command_map.items():
                    if command in text:
                        mainPlc.write_multiple_registers(5010, [40])
                        mainPlc.write_multiple_registers(5000, [value])
                        print(f"{value}개 주문이 실행되었습니다.")
                        print(f"{value}comp.")
                        return value
                print("명령어가 인식되지 않았습니다.")
                print("oder miss")
                return None
            except sr.UnknownValueError:
                print("음성을 명확하게 인식할 수 없습니다.")
                print("voice erro")
                return None
            except sr.RequestError as e:
                print(f"음성 인식 서비스에 접근할 수 없습니다: {e}")
                print(f"sservice not define: {e}")
                return None
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        print(f"er: {e}")
        return None


def index05(request):
    count = request.GET.get('count', 0)  # URL 파라미터에서 count 값을 가져옵니다.
    return render(request, './ramen/new_index05.html', {'count': count})
