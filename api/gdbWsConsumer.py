from channels.generic.websocket import WebsocketConsumer
import json
from api.gdbmiManager import manager


class Consumer(WebsocketConsumer):
    def connect(self):
        print('ws connected')
        self.client_id = self.scope['url_route']['kwargs']['client_id']
        self.accept()
        self.send(json.dumps(manager.connect(self.client_id)))

    def disconnect(self, code):
        print('ws disconnected')
        manager.disconnect(self.client_id)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        pid = text_data_json['pid']
        method = text_data_json['method']
        gdb_subprocess = manager.connect_to_gdb_subprocess(self.client_id, pid)
        status = gdb_subprocess['status']
        resp = ''
        if status:
            controller = gdb_subprocess['controller']
            try:
                if method == 'file':
                    # TODO upload elf
                    resp = controller.write('file demo')
                elif method == 'start':
                    resp = controller.write('start')
                elif method == 'next':
                    resp = controller.write('next')
            except Exception as e:
                status = 0
                resp = e
        else:
            resp = gdb_subprocess['msg']
        self.send(text_data=json.dumps({
            'status': status,
            'client_id': self.client_id,
            'pid': gdb_subprocess['pid'],
            'gdb_nums': gdb_subprocess['gdb_nums'],
            'resp': resp
        }))
