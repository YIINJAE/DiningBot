from django.shortcuts import render
from django.http import JsonResponse
from ..models import OrderStatus

# 주문 상태를 표시하는 뷰
def order_status_view(request):
    # remaining_count가 0인 주문들 중 status가 PREPARING인 경우에만 필터링
    completed_orders = OrderStatus.objects.filter(remaining_count=0, status='PREPARING').order_by('created_at')[:8]

    # remaining_count가 0보다 큰 준비 중인 주문들
    preparing_orders = OrderStatus.objects.filter(remaining_count__gt=0).order_by('created_at')[:8]

    # 각 패널에 8개의 셀을 맞추기 위해 빈 셀을 추가
    empty_completed_cells = 8 - len(completed_orders)
    empty_preparing_cells = 8 - len(preparing_orders)

    context = {
        'preparing_orders': preparing_orders,
        'completed_orders': completed_orders,
        'empty_completed_cells': range(empty_completed_cells),
        'empty_preparing_cells': range(empty_preparing_cells)
    }

    return render(request, 'ramen/order_status.html', context)

# Ajax 요청에 응답하여 remaining_count > 0인 주문을 반환하는 뷰
def get_active_orders(request):
    active_orders = OrderStatus.objects.filter(remaining_count__gt=0).values('id', 'employee_id', 'remaining_count')
    return JsonResponse(list(active_orders), safe=False)
