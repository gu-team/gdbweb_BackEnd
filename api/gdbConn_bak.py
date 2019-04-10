import os
from socket import *
from django.http import HttpResponse, JsonResponse

class Client:
    HOST = 'localhost'
    PORT = 8001
    BUFSIZ = 1024
    Conn = object()

    def connect(self):
        # 创建一个socket对象，AF_INET指定使用IPv4协议(AF_INET6代表IPV6)，SOCK_STREAM指定使用面向流的TCP协议
        self.Conn = socket(AF_INET, SOCK_STREAM)
        self.Conn.connect((self.HOST, self.PORT)) # 连接gdb服务器

    def disconnect(self):
        self.Conn.close()

    def send(self, command):
        self.Conn.send(command.encode('utf-8'))    # 对字符串进行字节编码，并发送
        resp = self.Conn.recv(self.BUFSIZ)         # 接受返回字节流
        return resp.decode('utf-8')                # 对返回的字节进行字符串编码


def start(request):
    client = Client()
    client.connect()
    resp = client.send('start')
    client.disconnect()

    retMsg = {
        'code': 0,
        'message': resp,
    }
    return JsonResponse(retMsg)


def continu(request):
    client = Client()
    client.connect()
    resp = client.send('continue')
    client.disconnect()

    retMsg = {
        'code': 0,
        'message': resp
    }
    return JsonResponse(retMsg)
