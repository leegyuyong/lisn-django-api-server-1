from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('v1/api/signin/', include('api.user.urls')),
    path('v1/api/record/', include('api.record.urls')),
]

if settings.DEBUG:
    def serve_index_html(request):
        return render(request, 'index.html', {})
    urlpatterns += [
        path('', serve_index_html),
        path('list', serve_index_html),
        path('note', serve_index_html),
    ]