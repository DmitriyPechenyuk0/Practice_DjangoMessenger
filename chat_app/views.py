from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views.generic import ListView, FormView
from django.http import HttpResponseForbidden
# from django.contrib.auth.models import User
# from user_app.models import Profile
from django.contrib.auth import get_user_model

Profile = get_user_model()

from .forms import MessageForm
from .models import ChatGroup, ChatMessage


class ChatView(FormView):
    '''
    Відображення конкретної чат групи
    '''
    # Вказуємо html-шаблон
    template_name = 'chat_app/chat.html'
    # Вказуємо форму для відображення сторінці
    form_class = MessageForm
    
    def dispatch(self, request, *args, **kwargs):
        '''Метод dispatch обробляє GET та POST запити'''
        # Отримуємо pk групи з динамічної адреси
        group_pk = self.kwargs['group_pk']
        # Отримуємо клас групи
        chat_group = ChatGroup.objects.get(pk = group_pk)
        # Перевіряємо, чи знаходится користувач в групі
        if request.user not in chat_group.members.all():
            # Видаємо помилку, що немає доступа
            return HttpResponseForbidden('<h1>У Вас немає доступу до цього чату</h1>')
        # Отримуємо список всіх повідомлень з цієї групи та перебираємо його
        for message in ChatMessage.objects.filter(chat_group = chat_group):
            # Додаємо поточного користувача до списку користувачів, котрі бачили це повідомлення
            if request.user != message.author:
                message.view_by_users.add(request.user)
            # Зберігаємо зміни до повідомлення у базу даних
            message.save()
        # Виклик dispatch (продовжууємо обробляти запит)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''
        Метод відповідаючий за формування context
        '''
        # отримуємо context
        context =  super().get_context_data(**kwargs) 
        # отримуємо pk групи з динамічної URL
        group_pk = self.kwargs['group_pk']
        # отримуємо групу по pk
        context['chat_group'] = ChatGroup.objects.get(pk = group_pk) 
        # отримуємо історію усіх повідомлень цієї групи
        context['message_history'] = ChatMessage.objects.filter(chat_group_id = group_pk)
        return context

class GroupListView(ListView):
    '''
        Клас відповідає за відображення сторінки груп
    '''
    # вказуємо модель, яку будемо перебирати
    model = ChatGroup
    # вказуємо, як буде називатися список у шаблоні
    context_object_name = 'group_list'
    # вказємо шаблонь який буде відоображатися
    template_name = 'chat_app/group_list.html'


class PersonalChatListView(ListView):
    '''
        Клас відповідає за відображення персональних чатів
    '''
    template_name = 'chat_app/personal_chat.html'
    context_object_name = 'persons'
    def get_queryset(self):
        '''
            Метод, що повертає список об'єктів, що будуть відображатись у шаблоні
        '''
        # отримуємо всіх користувачів, крім авторизованого
        return Profile.objects.exclude(pk = self.request.user.pk)

def redirect_to_personal_chat(request, user1_pk, user2_pk):
    '''
        перенаправлення до особистого чату між двома користувачами
    '''
    # отримуємо 1-ого користувача з динамічного url
    user1 = Profile.objects.get(pk = user1_pk)
    # отримуємо 2-ого користувача з динамічного url
    user2 = Profile.objects.get(pk = user2_pk)
    # шукаємо групу особистого чату між цими користувачами
    group : ChatGroup = ChatGroup.objects.filter(is_personal_chat = True).filter(members = user1).filter(members = user2).first()
    # перевіряємо, якщо особистого чату між цими користувачами немає
    if not group:
        # створюємо групу (особистий чат)
        group = ChatGroup.objects.create(name = f"Chats {user1}, {user2}", is_personal_chat = True)
        # додаємо користувачів до групи
        group.members.add(user1, user2)
        # зберігаємо зміни у групі
        group.save()
    # перенаправляємо користувача на сторінку цього персонального чату
    return redirect('chat', group.pk)
