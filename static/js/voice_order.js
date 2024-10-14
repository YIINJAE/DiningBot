document.addEventListener('DOMContentLoaded', function() {
    // 페이지가 로드되면 실행되는 코드. '.title' 클래스를 가진 요소를 선택
    const titleElement = document.querySelector('.title');

    // 타이틀 요소의 텍스트를 업데이트하는 함수
    function updateTitle(message) {
        titleElement.textContent = message;  // 타이틀 텍스트를 전달받은 메시지로 변경
    }

    // 음성 인식 요청을 서버에 보내는 함수
    function startVoiceRecognition() {
        // 서버에 '/Ramen/test-microphone/'로 POST 요청을 보냄
        fetch("/Ramen/test-microphone/", {
            method: 'POST',  // POST 메서드를 사용
            headers: {
                'Content-Type': 'application/json',  // 요청의 콘텐츠 유형을 JSON으로 설정
                'X-CSRFToken': getCookie('csrftoken'),  // CSRF 토큰을 포함하여 보안 유지
            }
        })
        // 서버로부터 응답을 받은 후 JSON 데이터를 처리
        .then(response => response.json())
        .then(data => {
            // 서버 응답 상태가 'update'인 경우
            if (data.status === 'update') {
                updateTitle(data.message);  // 타이틀 메시지 업데이트
                setTimeout(startVoiceRecognition, 1000);  // 1초 후 다시 음성 인식을 시작
            }
            // 서버 응답 상태가 'redirect'인 경우 해당 URL로 리디렉션
            else if (data.status === 'redirect') {
                window.location.href = data.url;  // 지정된 URL로 페이지 이동
            }
        })
        // 오류가 발생하면 콘솔에 출력
        .catch(error => console.error('Error:', error));
    }

    // 음성 인식 요청을 시작
    startVoiceRecognition();

    // CSRF 토큰을 쿠키에서 가져오는 함수
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');  // 쿠키 문자열을 ';' 기준으로 분할
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();  // 각 쿠키 항목에서 공백 제거
                // 원하는 쿠키의 이름과 일치하는 경우 해당 쿠키의 값을 반환
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;  // 값을 찾으면 반복 종료
                }
            }
        }
        return cookieValue;  // 해당 쿠키 값 반환
    }
});
