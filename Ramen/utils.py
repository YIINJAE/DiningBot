# Ramen/utils.py

import logging

class IgnoreOrderStatusFilter(logging.Filter):
    def filter(self, record):
        # 로그 메시지에 "order_status" URL이 포함되어 있으면 로그 기록 제외
        return 'order_status' not in record.getMessage()
