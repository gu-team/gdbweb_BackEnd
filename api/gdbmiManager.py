from collections import defaultdict
from pygdbmi.gdbcontroller import GdbController


class GdbmiManager:
    def __init__(self):
        # key is client id and value is controller
        self.clients = defaultdict(list)

    '''
    @desc:
        client connects to the backend by random client id.
        在用户列表中添加该用户。
    @params:
        client_id: 用户id，由前端生成的唯一标识
    '''
    def connect(self, client_id):
        self.clients[client_id] = []
        return {
            'status_code': 1, # 状态码
            'msg': 'connected successfully', # 信息
            'client_id': client_id, # 用户唯一标识
            'gdb_nums': len(self.clients[client_id]) # 用户启用的gdb进程个数
        }

    '''
    @desc:
        连接该用户的某个pid对应的gdb子进程。
        若pid为0，则新建gdb子进程。
        若pid对应子进程不存在，则返回错误信息。
    @params:
        client_id: 用户id
        pid: gdb子进程id
    '''
    def connect_to_gdb_subprocess(self, client_id, pid):
        status_code = 1
        msg = ''
        # create new controller if pid is less than 0
        if pid <= 0:
            controller = GdbController(gdb_args=['--interpreter=mi2'])
            self.clients[client_id].append(controller)
            pid = controller.gdb_process.pid
        else:
            controller = self.get_controller(client_id, pid)
            # get controller by pid. if it is not exist, return error.
            if not controller:
                status_code = 0
                msg = 'no such gdb subprocess with pid {}'.format(pid)
                print(msg)

        return {
            'status_code': status_code, # 状态码，1成功，0失败
            'msg': msg, # 信息
            'pid': pid, # gdb子进程号
            'gdb_nums': len(self.clients[client_id]) # gdb数量
        }

    '''
    @desc:
        remove all gdb subprocess when client disconnected.
    @params:
        client_id: 用户id
    '''
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

    '''
    @desc:
        remove GdbController instance by pid
    @params:
        client_id
        pid
    '''
    def remove_controller(self, client_id, pid):
        for controller in self.clients[client_id]:
            if pid == controller.gdb_process.pid:
                controller.exit()
                return

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
        status_code = 1
        msg = 'run this command successfully'
        data = []
        try:
            resp = controller.write(command_line)
            for item in resp:
                if item['type'] == 'console' or item['type'] == 'log':
                    data.append(item['payload'])
        except Exception as e:
            status_code = 0
            print('gdb_run_command error: ', e)
            msg = 'gdbmi write fail'
        return {
            'status_code': status_code, # 状态码
            'msg': msg, # 信息
            'data': data # 数据
        }


manager = GdbmiManager()
