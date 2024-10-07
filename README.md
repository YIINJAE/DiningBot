# 😀Abiman | ENG | DINNIG BOT
---
## 1. 프로젝트 이름
- Abiman | ENG | DINING BOT  

---
## 2. 프로젝트 설명
- 협동 로봇을 이용한 라면 조리 시스템.
- 주문 및 결재를 위한 Web 서비스 구축.
---
## 3. 사용방법
- 준비된 QR Code를 이용하여 주문 페이지 접속.
- 일반주문 & 음성주문 선택 (음성주문 현재 제외).
- 주문 수량 입력후 확인
- 결재 정보란에 사원번호 및 비밀번호 입력.
	- 최초 로그인시에 비밀번호 변경기능
- 자동주문 완료.

## 4. 사용자추가방법
- data/users.csv 파일 사용자 추가(양식참고)
- python manage.py import_users data/users.csv
- 다음코드 실행 자동 사용자 등록진행

## 5. Docker server compose 방법
- 해당프로젝트 경로에서 cmd창에서 다음 코드 실행
- docker-compose up --build
- Container 이름 변경을 원하면 docker-compose.yml 파일에서 container_name 부분변경