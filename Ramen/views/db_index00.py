from django.shortcuts import render, get_object_or_404

def login_view(request):
    return render(request, './ramen/new_index.html')