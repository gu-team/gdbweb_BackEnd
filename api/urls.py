from django.urls import path, include
from . import gdbContr

urlpatterns = [
    path('uploadelf', gdbContr.uploadelf),
    path('start', gdbContr.start),
    path('continue', gdbContr.continue_gdb),
    path('disassemble', gdbContr.disassemble),
    path('break', gdbContr.break_gdb),
    path('next', gdbContr.next_gdb),
]
