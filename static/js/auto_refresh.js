// 3초 후에 페이지를 자동으로 새로고침하는 스크립트
setTimeout(function() {
    window.location.href = "http://192.168.1.210:30000/Ramen/order_status/";
}, 3000); // 3000ms = 3초

// // 화면을 업데이트하는 함수
// function fetchAndUpdateOrders() {
//     fetch('/Ramen/get_active_orders/')
//         .then(response => response.json())
//         .then(data => {
//             // 모든 셀들을 가져옴
//             const leftPanel = document.querySelector('.left-panel');
//             const rightPanel = document.querySelector('.right-panel');

//             // 현재 패널에 표시된 셀들을 모두 지웁니다 (첫 번째 주문 완료 / 준비 중 셀은 유지)
//             leftPanel.querySelectorAll('.cell').forEach((cell, index) => {
//                 if (index !== 0) cell.remove();
//             });

//             rightPanel.querySelectorAll('.cell').forEach((cell, index) => {
//                 if (index !== 0) cell.remove();
//             });

//             // 서버에서 가져온 데이터를 화면에 표시
//             data.forEach(order => {
//                 // 준비 중 상태일 경우 오른쪽 패널에 표시
//                 if (order.remaining_count > 0) {
//                     const newCell = document.createElement('div');
//                     newCell.classList.add('cell');
//                     newCell.textContent = order.employee_id;
//                     rightPanel.appendChild(newCell);
//                 }
//             });
//         })
//         .catch(error => console.error('Error fetching order data:', error));
// }

// // 1분마다 실행하여 데이터를 갱신
// setInterval(fetchAndUpdateOrders, 60000); // 60000ms = 1분

// // 페이지 로드 시에도 데이터 가져와 화면을 갱신
// fetchAndUpdateOrders();
