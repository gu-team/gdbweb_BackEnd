import os
import random
import string

from django.http import HttpResponse, JsonResponse
from gdbmiManager import manager


'''
@desc:
    上传elf文件接口，并在该用户数据中记录该文件
@params:
    file: 上传的文件
    client_id: 用户标识
'''
def upload_elf(request):
    if request.method != 'POST':
        return JsonResponse({'status': 1, 'message': 'method not allowed'}, status=405)
    file = request.FILES.get('file', None)
    client_id = request.POST.get('client_id', '')
    if client_id == '':
        return JsonResponse({'status': 1, 'message': 'not client id'})
    if not file:
        return JsonResponse({'status': 1, 'message': 'file not found'})
    file_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    # os.getcwd() 获取脚本运行的目录(项目根目录)
    # os.path.join() 路径拼接
    with open(os.path.join(os.getcwd(), 'upload', file_name), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    manager.add_elf(client_id, file_name) # 记录进该用户上传的elf文件列表中
    return JsonResponse({
        'status': 0,
        'file_name': file_name})


'''
@desc:
    设置对应gdb子进程所调试程序的输入
@params:
    input_data: 程序输入数据
    pid: gdb进程号
'''
def set_input(request):
    # 如果不是POST请求，返回错误
    if request.method != 'POST':
        return JsonResponse({'status': 2, 'message': 'method not allowed'}, status=405)
    input_data = request.POST.get('input_data', '')
    pid = request.POST.get('pid', -1)
    print('set_inpit() receive ---> ', pid, input_data)
    # 如果pid为-1，返回错误
    if pid == -1:
        return JsonResponse({'status': 0, 'msg': 'pid is -1'})
    file_name = pid + '_input.txt'
    with open(os.path.join(os.getcwd(), 'upload', file_name), 'w') as f:
        f.write(input_data)
    return JsonResponse({
        'status': 0,
        'msg': 'set input successfully'})


'''
@desc:
    获取对应gdb子进程所调试程序的输出
@params:
    pid: gdb进程号
'''
def get_ouput(request):
    pid = request.GET.get('pid', -1)
    print('get_ouput() receive ---> ', pid)
    # 如果pid为-1，返回错误
    if pid == -1:
        return JsonResponse({'status': 0, 'msg': 'pid is -1'})
    file_name = pid + '_output.txt'
    with open(os.path.join(os.getcwd(), 'upload', file_name), 'r') as f:
        data = f.read()
    return JsonResponse({
        'status': 0,
        'msg': 'set input successfully',
        'data': data})
