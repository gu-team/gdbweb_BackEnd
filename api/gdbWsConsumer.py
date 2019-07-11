'''
继承 WebsocketConsumer ，负责WebSocket连接的处理(相当于controller)
'''
from channels.generic.websocket import WebsocketConsumer
import json
from api.gdbmiManager import manager


class Consumer(WebsocketConsumer):
    # WebSocket 连接
    def connect(self):
        print('ws connected')
        self.client_id = self.scope['url_route']['kwargs']['client_id']
        self.accept()
        self.send(json.dumps(manager.connect(self.client_id)))

    # WebSocket 断开连接
    def disconnect(self, code):
        print('ws disconnected')
        manager.disconnect(self.client_id)

    # WebSocket 数据接受处理
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data) # 处理接受到的数据
        command_line = text_data_json['command_line']
        pid = text_data_json['pid']
        connect_resp = manager.connect_to_gdb_subprocess(self.client_id, pid) # 连接gdb子进程，若没有则新建，若不存在则返回错误
        status = connect_resp['status']
        # if connect success
        if status:
            pid = connect_resp['pid']
            # if upload the elf
            if command_line == 'uploadelf':
                # TODO
                run_resp = manager.gdb_run_command('file demo', self.client_id, pid)
            else:
                run_resp = manager.gdb_run_command(command_line, self.client_id, pid)
            data = run_resp['data']
            status = run_resp['status']
            msg = run_resp['msg']
        # if connect fail
        else:
            msg = connect_resp['msg']

        self.send(text_data=json.dumps({
            'status': status,
            'msg': msg,
            'data': data,
            'client_id': self.client_id,
            'pid': pid,
            'gdb_nums': connect_resp['gdb_nums']
        }))
