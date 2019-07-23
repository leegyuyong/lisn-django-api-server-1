from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_html, name='index_html'),
    path('record/', views.save_record_and_response_stt_text, name='save_record_and_response_stt_text'),
]