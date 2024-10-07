from django import template

register = template.Library()

@register.filter
def get_range(value, max_count):
    """ value만큼 반복문을 돌리고 남는 갯수를 반환한다 """
    return range(max_count - value)
