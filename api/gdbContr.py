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
    ret['message'] = []
    for msg in resp:
        if msg['type'] == 'console' or msg['type'] == 'log':
            ret['message'].append(msg['payload'])

    print('ret------------> '+str(ret))
    return JsonResponse(ret)


def start(request):
    print('==============start==================')
    ret = {}
    pid = request.session.get('pid', -1)    # 先从session中拿到pid
    # print('pid: ' + request.COOKIES['sessionid'])
    if pid == -1:
        ret['code'] = 0
        ret['message'] = 'please upload elf first.'
    else:
        gdbmi = gdbmis.get(pid, -1)         # 用pid到gdbmis中拿到当前用户的gdbmi
        if gdbmi == -1:
            ret['code'] = 0
            ret['message'] = 'Error: no gdbmi of this pid in gdbmis'
        else:
            try:
                resp = gdbmi.write('start')
                ret['code'] = 1
                ret['message'] = []
                for msg in resp:
                    if msg['type'] == 'console' or msg['type'] == 'log':
                        ret['message'].append(msg['payload'])
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)                # 返回json化数据


# continue 继续程序
def continue_gdb(request):
    print('==============continu==================')
    ret = {}
    pid = request.session.get('pid', -1)    # 先从session中拿到pid
    if pid == -1:
        ret['code'] = 0
        ret['message'] = 'please upload elf first.'
    else:
        gdbmi = gdbmis.get(pid, -1)         # 用pid到gdbmis中拿到当前用户的gdbmi
        if gdbmi == -1:
            ret['code'] = 0
            ret['message'] = 'no gdbmi of this pid in gdbmis'
        else:
            try:
                resp = gdbmi.write('continue')
                ret['code'] = 1
                ret['message'] = []
                for msg in resp:
                    if msg['type'] == 'console' or msg['type'] == 'log':
                        ret['message'].append(msg['payload'])
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process. please upload elf first.'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)


# 返回汇编代码
def disassemble(request):
    print('==============disass==================')
    ret = {}
    fun_name = request.POST.get('funName')
    if fun_name is None:
        fun_name = ''

    pid = request.session.get('pid', -1)    # 先从session中拿到pid
    if pid == -1:
        ret['code'] = 0
        ret['message'] = 'please upload elf first.'
    else:
        gdbmi = gdbmis.get(pid, -1)         # 用pid到gdbmis中拿到当前用户的gdbmi
        if gdbmi == -1:
            ret['code'] = 0
            ret['message'] = 'no gdbmi of this pid in gdbmis'
        else:
            try:
                resp = gdbmi.write('disassemble ' + fun_name)
                ret['code'] = 1
                ret['message'] = []
                for msg in resp:
                    if msg['type'] == 'console' or msg['type'] == 'log':
                        ret['message'].append(msg['payload'])
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process. please upload elf first.'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)


# break下断点
def break_gdb(request):
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
        ret['message'] = 'please upload elf first.'
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
                resp = gdbmi.write(command)
                ret['code'] = 1
                ret['message'] = []
                for msg in resp:
                    if msg['type'] == 'console' or msg['type'] == 'log':
                        ret['message'].append(msg['payload'])
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process. please upload elf first.'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)


# next下一步
def next_gdb(request):
    print('==============next==================')
    ret = {}

    pid = request.session.get('pid', -1)    # 先从session中拿到pid
    if pid == -1:
        ret['code'] = 0
        ret['message'] = 'please upload elf first.'
    else:
        gdbmi = gdbmis.get(pid, -1)         # 用pid到gdbmis中拿到当前用户的gdbmi
        if gdbmi == -1:
            ret['code'] = 0
            ret['message'] = 'no gdbmi of this pid in gdbmis'
        else:
            try:
                resp = gdbmi.write('next')
                ret['code'] = 1
                ret['message'] = []
                for msg in resp:
                    if msg['type'] == 'console' or msg['type'] == 'log':
                        ret['message'].append(msg['payload'])
            except NoGdbProcessError:
                ret['code'] = 0
                ret['message'] = 'no gdb process. please upload elf first.'

    print('ret------------> '+str(ret))
    return JsonResponse(ret)
