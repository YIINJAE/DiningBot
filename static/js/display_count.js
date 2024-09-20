document.addEventListener('DOMContentLoaded', function() {
    // URL에서 count와 employee_id 값을 가져옵니다.
    const pathSegments = window.location.pathname.split('/');
    const count = pathSegments[3] || 0; // count는 URL의 세 번째 세그먼트에 위치합니다.

    // count 값을 화면에 표시합니다.
    document.getElementById('displayCount').textContent = count;

    // 일정 시간이 지나면 redirectUrl로 리다이렉트합니다.
    setTimeout(function() {
        window.location.href = redirectUrl + `?count=${count}`;
    }, 5000);  // 2초 후 리다이렉트
});
