from django.conf.urls import url
from django.urls import path, include

from api import gdbWsConsumer
from . import gdbContr

urlpatterns = [
    path('uploadelf', gdbContr.uploadelf),
    path('start', gdbContr.start),
    path('continue', gdbContr.continue_gdb),
    path('disassemble', gdbContr.disassemble),
    path('break', gdbContr.break_gdb),
    path('next', gdbContr.next_gdb),
]

websocket_urlpatterns = [
    # url(r'^ws/gdb/(?P<client_id>[^/]+)/$', gdbWsConsumer.Consumer),
    path('ws/gdb/<client_id>', gdbWsConsumer.Consumer)
]
