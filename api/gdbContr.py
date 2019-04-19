from django.http import HttpResponse, JsonResponse
from pygdbmi.gdbcontroller import GdbController, NoGdbProcessError

gdbmis = {}

def uploadelf(request):
    print('============uploadelf================')
    ret = {}
    fileName = request.GET.get('fileName')      # 从请求获取文件名参数
    if not fileName:
        fileName = 'demo'
    gdbmi = GdbController()                     # 为当前用户实例化GdbController对象
    # if gdbmi == None ???

    gdbmis[gdbmi.gdb_process.pid] = gdbmi          # 当前用户的gdbmi的pid作为 gdbmis 的key
    request.session['pid'] = gdbmi.gdb_process.pid  # 将pid放到当前用户的session中
    
    resp = gdbmi.write('file '+fileName)        # 加载调试文件，此时gdb还没有子进程，不需要抛出异常
    ret['code'] = 1
    ret['message'] = resp

    print('ret------------> '+str(ret))
    return JsonResponse(ret)


def start(request):
    print('==============start==================')
    ret = {}
    pid = request.session.get('pid', -1)    # 先从session中拿到pid
    if pid == -1:
        ret['code'] = 0
        ret['message'] = 'no pid in session'
    else:
        gdbmi = gdbmis.get(pid, -1)         # 用pid到gdbmis中拿到当前用户的gdbmi
        if gdbmi == -1:
            ret['code'] = 0
            ret['message'] = 'no gdbmi of this pid in gdbmis'
        else:
            try:
                ret['message'] = gdbmi.write('start')
                ret['code'] = 1
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)                # 返回json化数据


# continue 继续程序
def continu(request):
    print('==============continu==================')
    ret = {}
    pid = request.session.get('pid', -1)    # 先从session中拿到pid
    if pid == -1:
        ret['code'] = 0
        ret['message'] = 'no pid in session'
    else:
        gdbmi = gdbmis.get(pid, -1)         # 用pid到gdbmis中拿到当前用户的gdbmi
        if gdbmi == -1:
            ret['code'] = 0
            ret['message'] = 'no gdbmi of this pid in gdbmis'
        else:
            try:
                ret['message'] = gdbmi.write('continue')
                ret['code'] = 1
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)


# 返回汇编代码
def disass(request):
    print('==============disass==================')
    ret = {}
    fun_name = ''
    if request.method == 'POST':
        fun_name = request.POST.get('funName')

    pid = request.session.get('pid', -1)    # 先从session中拿到pid
    if pid == -1:
        ret['code'] = 0
        ret['message'] = 'no pid in session'
    else:
        gdbmi = gdbmis.get(pid, -1)         # 用pid到gdbmis中拿到当前用户的gdbmi
        if gdbmi == -1:
            ret['code'] = 0
            ret['message'] = 'no gdbmi of this pid in gdbmis'
        else:
            try:
                ret['message'] = gdbmi.write('disassemble ' + fun_name)
                ret['code'] = 1
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)


# break下断点
def brea(request):
    print('==============break==================')
    ret = {}
    typ = 0
    msg = ''
    if request.method == 'POST':
        typ = request.POST.get('type')
        msg = request.POST.get('message')

    pid = request.session.get('pid', -1)    # 先从session中拿到pid
    if pid == -1:
        ret['code'] = 0
        ret['message'] = 'no pid in session'
    else:
        gdbmi = gdbmis.get(pid, -1)         # 用pid到gdbmis中拿到当前用户的gdbmi
        if gdbmi == -1:
            ret['code'] = 0
            ret['message'] = 'no gdbmi of this pid in gdbmis'
        else:
            try:
                command = 'break ' + msg
                # 如果是对十六进制地址下断点
                if typ == 2:
                    command = 'break *' + msg
                ret['message'] = gdbmi.write(command)
                ret['code'] = 1
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)