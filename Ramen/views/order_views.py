from django.shortcuts import render
from django.http import JsonResponse
from ..models import OrderStatus

# 주문 상태를 표시하는 뷰
def order_status_view(request):
    preparing_orders = OrderStatus.objects.filter(remaining_count__gt=0)
    completed_orders = OrderStatus.objects.filter(remaining_count=0)

    context = {
        'preparing_orders': preparing_orders,
        'completed_orders': completed_orders
    }

    return render(request, 'ramen/order_status.html', context)

# Ajax 요청에 응답하여 remaining_count > 0인 주문을 반환하는 뷰
def get_active_orders(request):
    active_orders = OrderStatus.objects.filter(remaining_count__gt=0).values('id', 'employee_id', 'remaining_count')
    return JsonResponse(list(active_orders), safe=False)
