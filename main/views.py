from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def get_main_page(request):
    return render(request, 'main/index.html', {})