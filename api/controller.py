import os
import random
import string

from django.http import HttpResponse, JsonResponse

def upload_elf(request):
    if request.method != 'POST':
        return JsonResponse({'status': 1, 'message': 'method not allowed'}, status=405)
    file = request.FILES.get('file', None)
    client_id = request.POST.get('client_id', '')
    if client_id == '':
        return JsonResponse({'status': 1, 'message': 'not client id'})
    if not file:
        return JsonResponse({'status': 1, 'message': 'file not found'})
    filename = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    with open(os.path.join(os.getcwd(), 'upload', filename), 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    
    return JsonResponse({
        'status': 0,
        'filename': filename})


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
    filename = pid + '_input.txt'
    with open(os.path.join(os.getcwd(), 'upload', filename), 'w') as f:
        f.write(input_data)
    return JsonResponse({
        'status': 0,
        'msg': 'set input successfully'})


def get_ouput(request):
    pid = request.GET.get('pid', -1)
    print('get_ouput() receive ---> ', pid)
    # 如果pid为-1，返回错误
    if pid == -1:
        return JsonResponse({'status': 0, 'msg': 'pid is -1'})
    filename = pid + '_output.txt'
    with open(os.path.join(os.getcwd(), 'upload', filename), 'r') as f:
        data = f.read()
    return JsonResponse({
        'status': 0,
        'msg': 'set input successfully',
        'data': data})
