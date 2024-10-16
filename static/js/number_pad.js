let activeInput = null;

// 클릭 시 키패드 보이기
function showNumberPad(inputId) {
    document.getElementById('number-pad').style.display = 'block';
    activeInput = document.getElementById(inputId);  // 현재 선택된 입력 필드 설정
}

// 선택된 입력 필드에 숫자 추가
function addNumber(number) {
    if (activeInput) {
        activeInput.value += number;
    }
}

// 마지막 글자 지우기 (지우기 버튼 기능 추가)
function deleteLastChar() {
    if (activeInput && activeInput.value.length > 0) {
        activeInput.value = activeInput.value.slice(0, -1);  // 입력 필드의 마지막 문자를 제거
    }
}

// Enter 버튼 클릭 시 입력 완료
function submitInput() {
    document.getElementById('number-pad').style.display = 'none';  // 키패드 숨기기
}

// 키패드 외부를 클릭했을 때 키패드를 닫음
document.addEventListener('click', function(event) {
    const numberPad = document.getElementById('number-pad');
    if (!event.target.closest('.number-pad') && !event.target.closest('.input-field')) {
        numberPad.style.display = 'none';
    }
});
