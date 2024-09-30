document.addEventListener('DOMContentLoaded', function() {
    const titleElement = document.querySelector('.title');

    function updateTitle(message) {
        titleElement.textContent = message;
    }

    function startVoiceRecognition() {
        fetch("/Ramen/test-microphone/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'update') {
                updateTitle(data.message);
                setTimeout(startVoiceRecognition, 1000);  // 딜레이 후 다음 단계로 이동
            } else if (data.status === 'redirect') {
                window.location.href = data.url;
            }
        })
        .catch(error => console.error('Error:', error));
    }

    startVoiceRecognition();

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
