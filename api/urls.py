from django.urls import path, include
from . import gdbContr

urlpatterns = [
    path('uploadelf', gdbContr.uploadelf),
    path('start', gdbContr.start),
    path('continue', gdbContr.continu),
]