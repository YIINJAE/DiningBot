from django.http import JsonResponse
from ..models import OrderStatus

def get_active_orders(request):
    # 모든 주문을 가져오고 remaining_count 값도 함께 반환합니다
    active_orders = OrderStatus.objects.values('id', 'employee_id', 'remaining_count')
    return JsonResponse(list(active_orders), safe=False)
