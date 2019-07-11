from collections import defaultdict
from pygdbmi.gdbcontroller import GdbController


class GdbmiManager:
    def __init__(self):
        # key is client id and value is controller
        self.clients = defaultdict(list)

<<<<<<< HEAD
    '''
    @desc:
        client connects to the backend by random client id.
        在用户列表中添加该用户。
    @params:
        client_id: 用户id，由前端生成的唯一标识
    '''
=======
    # client connects to the backend by random client id
>>>>>>> e7175a3... use websocket to connect, this is a simple demo
    def connect(self, client_id):
        self.clients[client_id] = []
        return {
            'status': 1,
<<<<<<< HEAD
            'msg': 'connected successfully',
=======
            'msg': 'connected',
>>>>>>> e7175a3... use websocket to connect, this is a simple demo
            'client_id': client_id,
            'gdb_nums': len(self.clients[client_id])
        }

<<<<<<< HEAD
    '''
    @desc:
        连接该用户的某个pid对应的gdb子进程。
        若pid为0，则新建gdb子进程。
        若pid对应子进程不存在，则返回错误信息。
    @params:
        client_id: 用户id
        pid: gdb子进程id
    '''
=======
>>>>>>> e7175a3... use websocket to connect, this is a simple demo
    def connect_to_gdb_subprocess(self, client_id, pid):
        status = 1
        msg = ''
        # create new controller if pid is less than 0
        if pid <= 0:
            controller = GdbController(gdb_args=['--interpreter=mi2'])
            self.clients[client_id].append(controller)
            pid = controller.gdb_process.pid
        else:
            controller = self.get_controller(client_id, pid)
<<<<<<< HEAD
            # get controller by pid. if it is not exist, return error.
            if not controller:
                status = 0
                msg = 'no such gdb subprocess with pid {}'.format(pid)
                print(msg)
=======
            if not controller:
                status = 0
                msg = 'no such gdb subprocess with pid {}'.format(pid)
>>>>>>> e7175a3... use websocket to connect, this is a simple demo

        return {
            'status': status,
            'msg': msg,
<<<<<<< HEAD
            'pid': pid,
            'gdb_nums': len(self.clients[client_id])
        }

    '''
    @desc:
        remove all gdb subprocess when client disconnected.
    @params:
        client_id: 用户id
    '''
=======
            'client_id': client_id,
            'pid': pid,
            'gdb_nums': len(self.clients[client_id]),
            'controller': controller
        }

    # remove all gdb subprocess when client disconnected
>>>>>>> e7175a3... use websocket to connect, this is a simple demo
    def disconnect(self, client_id):
        for controller in self.clients[client_id]:
            controller.exit()
        self.clients.pop(client_id)

    # get GdbController instance by pid
    def get_controller(self, client_id, pid):
        for controller in self.clients[client_id]:
            if pid == controller.gdb_process.pid:
                return controller
        return None

<<<<<<< HEAD
    '''
    @desc:
        remove GdbController instance by pid
    @params:
        client_id
        pid
    '''
=======
    # remove GdbController instance by pid
>>>>>>> e7175a3... use websocket to connect, this is a simple demo
    def remove_controller(self, client_id, pid):
        for controller in self.clients[client_id]:
            if pid == controller.gdb_process.pid:
                controller.exit()
                return

<<<<<<< HEAD
    '''
    @desc:
        调用 .write() 执行gdb命令，若异常则返回错误
    @params:
        command_line: gdb 的一行命令
        client_id
        pid
    '''
    def gdb_run_command(self, command_line, client_id, pid):
        controller = self.get_controller(client_id, pid)
        status = 1
        msg = 'run this command successfully'
        data = []
        try:
            resp = controller.write(command_line)
            for item in resp:
                if item['type'] == 'console' or item['type'] == 'log':
                    data.append(item['payload'])
        except Exception as e:
            status = 0
            print('gdb_run_command error: ', e)
            msg = 'gdbmi write fail'
        return {
            'status': status,
            'msg': msg,
            'data': data
        }

=======
>>>>>>> e7175a3... use websocket to connect, this is a simple demo

manager = GdbmiManager()
