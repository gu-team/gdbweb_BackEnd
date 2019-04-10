from django.http import HttpResponse, JsonResponse
from pygdbmi.gdbcontroller import GdbController, NoGdbProcessError

gdbmis = {}

def uploadelf(request):
    print('============uploadelf================')
    fileName = request.GET.get('fileName')
    if not fileName:
        fileName = 'demo'
    gdbmi = GdbController()
    resp = gdbmi.write('file '+fileName)
    print(resp)
    request.session['id'] = '1'
    gdbmis[request.session['id']] = gdbmi
    ret = {
        'code': 0,
        'message': resp,
    }
    print('ret------------> '+str(ret))
    return JsonResponse(ret)


def start(request):
    print('==============start==================')
    gdbmiId = request.session.get('id', -1)
    ret = {}
    if gdbmiId == -1:
        ret['code'] = 1
        ret['message'] = 'no gdbmi in session'
    else:
        gdbmi = gdbmis[gdbmiId]
        try:
            ret['message'] = gdbmi.write('start')
            ret['code'] = 0
        except NoGdbProcessError:
            ret['code'] = 1
            ret['message'] = 'no gdb process'
    return JsonResponse(ret)


def continu(request):
    print('==============continu==================')
    gdbmiId = request.session.get('id', -1)
    ret = {}
    if gdbmiId == -1:
        ret['code'] = 1
        ret['message'] = 'no gdbmi in session'
    else:
        gdbmi = gdbmis[gdbmiId]
        try:
            ret['message'] = gdbmi.write('continue')
            ret['code'] = 0
        except NoGdbProcessError:
            ret['code'] = 1
            ret['message'] = 'no gdb process'
    return JsonResponse(ret)
