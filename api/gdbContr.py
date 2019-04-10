from django.http import HttpResponse, JsonResponse
from pygdbmi.gdbcontroller import GdbController, NoGdbProcessError

# ret = {}

def uploadelf(request):
    print('============uploadelf================')
    fileName = request.GET.get('fileName')
    if not fileName:
        fileName = 'demo'
    gdbmi = GdbController()
    resp = gdbmi.write('file '+fileName)
    print(resp)
    # request.session['GdbController'] = gdbmi
    ret = {
        'code': 0,
        'message': resp,
    }
    print('ret------------'+str(ret))
    return JsonResponse(ret)

def start(request):
    print('==============start==================')
    gdbmi = request.session.get('GdbController')
    try:
        ret['message'] = gdbmi.write('start')
        ret['code'] = 0
    except NoGdbProcessError:
        ret['code'] = 1
        ret['message'] = 'no gdb process'
    return JsonResponse(ret)

def continu(request):
    print('==============continu==================')
    gdbmi = request.session.get('GdbController')
    try:
        ret['message'] = gdbmi.write('continue')
        ret['code'] = 0
    except NoGdbProcessError:
        ret['code'] = 1
        ret['message'] = 'no gdb process'
    return JsonResponse(ret)
