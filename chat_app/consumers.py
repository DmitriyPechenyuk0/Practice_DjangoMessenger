'''
Файл для обробки асинхронних підключень(веб-сокет)
'''
import json, datetime
from channels.generic.websocket import AsyncWebsocketConsumer

from .forms import MessageForm
from .models import ChatGroup, ChatMessage
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
# from .serializers import MessageSerializer

@sync_to_async
def get_views_count(message):
    return message.view_by_users.count()
class ChatConsumer(AsyncWebsocketConsumer):
    '''
    Клас для обробки Web-Socket запитів для роботи чату
    '''

    async def connect(self):
        '''
        Метод, що викликається при підключенні користувача до WebSocket
        '''
        # Зберігаємо у форматі str pk нашої групи (pk отримуємо з динамічної URL)
        self.room_group_name = str(self.scope['url_route']['kwargs']['group_pk']) 
        # Додаємо канал користувача до групи
        await self.channel_layer.group_add(
            #назва групи, до якої додається користувач
            self.room_group_name,
            # назва каналу поточного websocket з'єднаня
            self.channel_name
        )
        # Приймаємо WebSocket з'єднання
        await self.accept()

    async def receive(self, text_data):
        '''
        Отримуємо дані із форми повідомлення, та передаємо назад до клієнта, для відображення у чаті всіх повідомлень
        '''
        # Збереження зображення у БД (а також отримуємо об'єкт збереженого повідомлення у змінну)
        message_db = await self.save_message_to_db(text_data = text_data)
        # Відправлення дані повідомлення до групи
        print(message_db, '12321')
        await self.channel_layer.group_send(
            self.room_group_name,
            # event
            {
                'type': 'send_message_to_every_member', # тип події, що вказує на метод, який буде викликаний
                'text_data': text_data, #повідомлення в форматі json 
                "username": self.scope['user'].username, # Отримуємо ім'я користувача, який відправляє повідомлення
                "date_time": message_db.date_time, #час створення повідомлення
                "message": message_db
            }
        )
    
    async def send_message_to_every_member(self, event):
        '''
        Метод, який надсилає повідомлення кожному учаснику групи
        '''
        # Створюємо об'єкт форми для повідолмень та наповнює її даними
        form = MessageForm(json.loads(event['text_data']))
        #робимо перевірку форми
        try:
            #Якщо форма валідна 
            if form.is_valid():
                print('send')
                #Відправляємо повідомлення назад клієнту у форматі JSON
                # for user in 
                

                await self.send(text_data= json.dumps({
                    'type': 'chat',
                    'message': form.cleaned_data['message'], #текст повідомлення
                    'username': event["username"], # Отримуємо ім'я користувача, яке ми передали через метод receive та group_send
                    "date_time": event['date_time'].isoformat(), #дата та час у форматі iso
                    "views": await get_views_count(event['message'])
                }))
        except Exception as ERROR:
             # Виводимо помилку
            print(ERROR)
            # pass

    @database_sync_to_async
    def save_message_to_db(self, text_data):
        '''
            Зберігає повідомлення у БД в асинхронному режимі
        '''
        #Створюємо новий об'єкт ChatMessage та зберігаємо його у БД
        return ChatMessage.objects.create(
            content = json.loads(text_data)["message"],#отримуємо текст повідомлення з json
            author = self.scope['user'],#автор повідомлення - поточний користувач
            chat_group = ChatGroup.objects.get(pk = self.room_group_name)#група чату,до якої належать повідомлення 
        )
        