from django.http import JsonResponse, HttpResponseRedirect  # JsonResponse 및 리다이렉션 기능을 위한 모듈
from django.shortcuts import render, redirect  # 페이지 렌더링 및 리다이렉션을 위한 모듈
from pyModbusTCP.client import ModbusClient  # Modbus TCP 통신을 위한 모듈
import speech_recognition as sr  # 음성 인식을 위한 SpeechRecognition 모듈
import time  # 딜레이 및 시간 관련 모듈

# PLC IP 주소 설정 및 ModbusClient 인스턴스 생성
plc_ip = "192.168.1.10"
mainPlc = ModbusClient(host=plc_ip, unit_id=1, auto_open=True, auto_close=True)

# 음성 주문 페이지를 표시하는 뷰
def voice_oder(request):
    return render(request, './ramen/new_index03.html')  # 음성 주문을 위한 페이지 렌더링

# POST 요청을 통해 마이크 테스트 결과를 받아 처리하는 뷰
def test_microphone_view(request):
    if request.method == 'POST':
        result = test_microphone()  # 마이크 테스트 함수 실행
        if result:
            # 주문 성공 시, index05로 리다이렉트하면서 주문 수량 전달
            return JsonResponse({'status': 'redirect', 'url': f'/Ramen/index05/?count={result}'})
        else:
            # 주문 실패 시, index02로 리다이렉트
            return JsonResponse({'status': 'redirect', 'url': '/Ramen/index02/'})
    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'})  # 잘못된 요청 처리

# 음성 인식 및 주문 수량을 처리하는 함수
def test_microphone(device_index=None):
    recognizer = sr.Recognizer()  # 음성 인식을 위한 Recognizer 인스턴스 생성
    # 음성 명령어와 그에 해당하는 주문 수량을 매핑한 딕셔너리
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
    }

    try:
        # 마이크에서 음성을 수집
        with sr.Microphone(device_index=device_index) as source:
            recognizer.adjust_for_ambient_noise(source)  # 주변 소음에 맞게 마이크를 조정
            print("주문수량을 말씀해 주세요.")  # 사용자에게 안내
            audio = recognizer.listen(source)  # 음성을 듣고 오디오 객체로 변환
            time.sleep(2)  # 2초 지연

            try:
                print("주문 수량 확인중...")  # 주문 수량 확인 메시지
                # 구글 음성 인식 API를 통해 한국어 음성을 텍스트로 변환
                text = recognizer.recognize_google(audio, language="ko-KR")
                
                # 명령어와 일치하는 경우에 주문 수량을 PLC에 전송
                for command, value in command_map.items():
                    if command in text:
                        mainPlc.write_multiple_registers(5010, [40])  # PLC 명령 실행 (40)
                        mainPlc.write_multiple_registers(5000, [value])  # 주문 수량 PLC로 전송
                        print(f"{value}개 주문이 실행되었습니다.")  # 콘솔에 성공 메시지 출력
                        return value  # 주문 수량 반환
                # 명령어 인식 실패 시
                print("명령어가 인식되지 않았습니다.")
                return None
            except sr.UnknownValueError:
                # 음성 인식 실패 시 처리
                print("음성을 명확하게 인식할 수 없습니다.")
                return None
            except sr.RequestError as e:
                # 음성 인식 서비스에 문제가 있을 때 처리
                print(f"음성 인식 서비스에 접근할 수 없습니다: {e}")
                return None
    except Exception as e:
        # 예기치 않은 예외 발생 시 처리
        print(f"오류가 발생했습니다: {e}")
        return None

# 주문 완료 후 이동하는 페이지 (index05)
def index05(request):
    count = request.GET.get('count', 0)  # URL 파라미터에서 count 값을 가져옴
    return render(request, './ramen/new_index05.html', {'count': count})  # count 값을 전달하여 렌더링
