from django.conf.urls import url
from codenamez import consumers

urlpatterns = [
    url(r'^codenamez/game/$', consumers.GameConsumer),
]