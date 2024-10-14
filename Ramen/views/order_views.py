from django.shortcuts import render
from django.http import JsonResponse
from ..models import OrderStatus

# 주문 상태를 표시하는 뷰
def order_status_view(request):
    # remaining_count가 0이면서 status가 'PREPARING'인 주문들을 필터링하여 완료된 주문 목록을 만듭니다.
    # 주문들은 created_at 기준으로 정렬되며, 최대 8개까지만 표시됩니다.
    completed_orders = OrderStatus.objects.filter(remaining_count=0, status='PREPARING').order_by('created_at')[:8]

    # remaining_count가 0보다 큰 주문들을 필터링하여 준비 중인 주문 목록을 만듭니다.
    # 마찬가지로 created_at 기준으로 정렬되며, 최대 8개까지만 표시됩니다.
    preparing_orders = OrderStatus.objects.filter(remaining_count__gt=0).order_by('created_at')[:8]

    # 각 패널(완료된 주문과 준비 중인 주문)에 8개의 셀이 필요하므로, 부족한 셀을 채우기 위해 빈 셀의 개수를 계산합니다.
    empty_completed_cells = 8 - len(completed_orders)  # 완료된 주문 패널에 필요한 빈 셀의 개수
    empty_preparing_cells = 8 - len(preparing_orders)  # 준비 중인 주문 패널에 필요한 빈 셀의 개수

    # 템플릿에 전달할 데이터를 context에 담습니다.
    context = {
        'preparing_orders': preparing_orders,  # 준비 중인 주문 목록
        'completed_orders': completed_orders,  # 완료된 주문 목록
        'empty_completed_cells': range(empty_completed_cells),  # 완료된 주문 패널의 빈 셀
        'empty_preparing_cells': range(empty_preparing_cells)   # 준비 중인 주문 패널의 빈 셀
    }

    # ramen/order_status.html 템플릿을 렌더링하여 반환합니다.
    return render(request, 'ramen/order_status.html', context)

# Ajax 요청에 응답하여 remaining_count > 0인 주문 목록을 반환하는 뷰
def get_active_orders(request):
    # remaining_count가 0보다 큰 주문들만 필터링하여 JSON 형식으로 반환합니다.
    # 주문의 id, employee_id, remaining_count 값만 반환합니다.
    active_orders = OrderStatus.objects.filter(remaining_count__gt=0).values('id', 'employee_id', 'remaining_count')
    return JsonResponse(list(active_orders), safe=False)  # JSON 응답을 반환
