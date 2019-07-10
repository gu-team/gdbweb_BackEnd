from collections import defaultdict
from pygdbmi.gdbcontroller import GdbController


class GdbmiManager:
    def __init__(self):
        # key is client id and value is controller
        self.clients = defaultdict(list)

    # client connects to the backend by random client id
    def connect(self, client_id):
        self.clients[client_id] = []
        return {
            'status': 1,
            'msg': 'connected',
            'client_id': client_id,
            'gdb_nums': len(self.clients[client_id])
        }

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
            if not controller:
                status = 0
                msg = 'no such gdb subprocess with pid {}'.format(pid)

        return {
            'status': status,
            'msg': msg,
            'client_id': client_id,
            'pid': pid,
            'gdb_nums': len(self.clients[client_id]),
            'controller': controller
        }

    # remove all gdb subprocess when client disconnected
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

    # remove GdbController instance by pid
    def remove_controller(self, client_id, pid):
        for controller in self.clients[client_id]:
            if pid == controller.gdb_process.pid:
                controller.exit()
                return


manager = GdbmiManager()
