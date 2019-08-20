from django.conf.urls import url
from django.urls import path, include

from api import gdbWsConsumer
from . import controller

urlpatterns = [
    path('uploadElf', controller.upload_elf),
    path('setInput', controller.set_input),
    path('getOutput', controller.get_ouput),
]

# websocket 路由映射
websocket_urlpatterns = [
    path('ws/gdb/<client_id>', gdbWsConsumer.Consumer)
]
