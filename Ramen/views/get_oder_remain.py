from django.http import JsonResponse  # JSON 응답을 반환하기 위한 Django 모듈
from ..models import OrderStatus  # OrderStatus 모델을 가져옴

# 활성화된 주문(remaining_count 값을 포함)을 가져오는 뷰 함수
def get_active_orders(request):
    # 모든 OrderStatus 객체에서 id, employee_id, remaining_count 필드를 가져옵니다.
    # values() 메소드를 사용하여 필요한 필드만 가져옴 (id, employee_id, remaining_count)
    active_orders = OrderStatus.objects.values('id', 'employee_id', 'remaining_count')

    # QuerySet을 리스트로 변환한 후, JSON 응답으로 반환
    # JsonResponse를 통해 리스트 형식의 데이터를 JSON 형식으로 변환하고 반환
    # safe=False는 리스트 형식의 데이터를 안전하게 전달하기 위해 사용
    return JsonResponse(list(active_orders), safe=False)
