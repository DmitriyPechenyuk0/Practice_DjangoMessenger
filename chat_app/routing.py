'''
Відповідає за визначення маршрутів та обробку запитів по протоколу веб-сокет
'''
from django.urls import path 
from .consumers import ChatConsumer

# Встановлюємо список маршутів
ws_urlpatterns = [
    # Встановлюємо  динамічну url для чату, передаючи pk групи, до якої хочемо підключитись
    path(route= 'chat/<int:group_pk>', view= ChatConsumer.as_asgi()),
]