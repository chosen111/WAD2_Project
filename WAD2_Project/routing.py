### This file is used with channels, disabled for this project
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import codenamez.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            codenamez.routing.urlpatterns
        )
    ),
})