from django.urls import path, include
from . import gdbConn

urlpatterns = [
    path('start', gdbConn.start),
    path('continue', gdbConn.continu),
]