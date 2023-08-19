from django.urls import path
from .views import *
urlpatterns = [
    path('<str:group_name>', index),
    path('views/send_dynamic_msg_to_group', send_dynamic_msg_to_group ),
]