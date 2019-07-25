from django.shortcuts import render

def signin_html(request):
    return render(request, 'signin/signin.html', {})