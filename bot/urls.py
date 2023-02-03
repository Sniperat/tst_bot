from django.urls import path
from .views import event, SendView, ChatView

app_name = 'bot'

urlpatterns = [
    path('', event),
    path("send/", SendView.as_view(), name="send"),
    path("chat/<int:id>/", ChatView.as_view(), name="chat")
]
