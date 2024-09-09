'''
24.09.09
'''
from django.shortcuts import render, get_object_or_404


#메인 화면 첫화면

def index(request):
    return render(request, './ramen/new_index.html')
