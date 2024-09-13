document.addEventListener('DOMContentLoaded', function() {
    var countElement = document.getElementById('count');
    var count = parseInt(countElement.textContent);

    document.getElementById('increase').addEventListener('click', function(e) {
        e.preventDefault();
        if (count < 9) {  // count가 9보다 작을 때만 증가시킵니다.
            count++;
            countElement.textContent = count;
        }
    });

    document.getElementById('decrease').addEventListener('click', function(e) {
        e.preventDefault();
        if (count > 0) {  // count가 0보다 클 때만 감소시킵니다.
            count--;
            countElement.textContent = count;
        }
    });

    document.getElementById('confirm').addEventListener('click', function(e) {
        e.preventDefault();
        var confirmUrl = this.getAttribute('data-confirm-url');
        var url = confirmUrl + "?count=" + count;
        window.location.href = url;
    });
});
