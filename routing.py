'''
WebSocket配置。将路由定义与 api.urls.websocket_urlpatterns 关联
'''
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import api

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            api.urls.websocket_urlpatterns
        )
    ),
})
