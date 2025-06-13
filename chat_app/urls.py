from .views import (
    # render_chat, 
    GroupListView,
    ChatView,
    PersonalChatListView,
    redirect_to_personal_chat
)
from django.urls import path


urlpatterns = [
    # path(route = 'chat/<int:group_pk>', view = render_chat, name = 'chat'),
    path(route = 'chat/<int:group_pk>', view = ChatView.as_view(), name = 'chat'),
    path(route='', view=GroupListView.as_view(), name = 'chat_groups'),
    path(route= 'personal_chat/', view= PersonalChatListView.as_view(), name= 'personal_chats'),
    path(route= 'to_personal_chat/<int:user1_pk>/<int:user2_pk>', view= redirect_to_personal_chat, name= 'to_personal_chat'),
]
    
