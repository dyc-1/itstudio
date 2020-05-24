from django.urls import path, include
from api.views import *

urlpatterns = [
    # 不带斜杠的url链接
    path('code', code, name="code"),
    path('register', register, name="register"),
    path('check', check, name="check"),
    path('department', department, name='department'),
    path('member', member, name='member'),
    path('history', history, name='history'),
    path('work', work, name='work'),
    path('comment', comment, name='comment'),
    path('data_init', data_init, name='data_init'),
    path('export', exportToExcel, name='exportToExcel'),
    path('get/ip', get_ip_json, name='get_ip_json'),

    # 带斜杠的url链接
    path('code/', code, name="code"),
    path('register/', register, name="register"),
    path('check/', check, name="check"),
    path('department/', department, name='department'),
    path('member/', member, name='member'),
    path('history/', history, name='history'),
    path('work/', work, name='work'),
    path('comment/', comment, name='comment'),
    path('data_init/', data_init, name='data_init'),
    path('export/', exportToExcel, name='exportToExcel'),
    path('get/ip/', get_ip_json, name='get_ip_json'),
]
