'''
继承 WebsocketConsumer ，负责WebSocket连接的处理(相当于controller)
'''
import os

from channels.generic.websocket import WebsocketConsumer
import json
from api.gdbmiManager import manager


class Consumer(WebsocketConsumer):
    # WebSocket 连接
    def connect(self):
        print('ws connected')
        self.SUCCESS_CODE = 0
        self.ERROR_CODE = 1  # 错误状态码，通常由于程序自身原因
        self.FAIL_CODE = 2  # 失败状态码，通常由于请求参数错误
        self.client_id = self.scope['url_route']['kwargs']['client_id']
        self.accept()
        resp = manager.connect(self.client_id)
        resp['status_code'] = self.SUCCESS_CODE
        self.send(json.dumps(resp))

    # WebSocket 断开连接
    def disconnect(self, code):
        print('ws disconnected')
        manager.disconnect(self.client_id)

    # WebSocket 数据接受处理
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data) # json化处理接受到的数据
        command_line = text_data_json.get('command_line', 'quit') # 要发送的命令行参数
        pid = text_data_json.get('pid', -1) # 对应的gdb进程号
        data_flag = text_data_json.get('data_flag', 'none') # 数据标识，原封不动传回前端，用于前端识别不同数据
        file_name = text_data_json.get('file_name', '') # 输入上传程序名
        print('receive ---> ', command_line, pid, data_flag, file_name)

        status_code = self.SUCCESS_CODE

        # 连接gdb子进程，若没有则新建，若不存在则返回错误
        connect_resp = manager.connect_to_gdb_subprocess(self.client_id, pid)
        # 如果连接gdb子进程成功
        if connect_resp['isSuccess']:
            pid = connect_resp['pid']
            if command_line == 'start' or command_line == 'next':
                command_line += ' < ' + pid + '_input.txt > ' + pid + '_output.txt'
            if command_line == 'file':
                print(os.path.join(os.getcwd(), 'upload', file_name))
                run_resp = manager.gdb_run_command(
                    'file ' + os.path.join(os.getcwd(), 'upload', file_name),
                    self.client_id,
                    pid)
            run_resp = manager.gdb_run_command(command_line, self.client_id, pid)
            data = run_resp['data']
            msg = run_resp['msg']
            if not run_resp['isSuccess']:
                status_code = self.ERROR_CODE

        # 如果连接gdb子进程失败
        else:
            msg = connect_resp['msg']
            status_code = self.FAIL_CODE

        self.send(text_data=json.dumps({
            'status_code': status_code,  # 状态码
            'msg': msg,  # 信息
            'data': data,  # 数据
            'data_flag': data_flag,  # 数据标识
            'client_id': self.client_id,  # 用户唯一标识
            'pid': pid,  # 当前gdb子进程号
            'gdb_nums': connect_resp['gdb_nums']  # 用户所启动的gdb个数
        }))
