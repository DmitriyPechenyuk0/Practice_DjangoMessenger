from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
# from user_app.models import Profile
Profile = get_user_model()

# Create your models here.
class ChatGroup(models.Model):
    name = models.CharField(max_length = 255)
    members = models.ManyToManyField(Profile)
    is_personal_chat = models.BooleanField(default= False) #
    
    def __str__(self):
        return f'Група -> {self.name}'
    
    def get_absolute_url(self):
        return reverse("chat", kwargs={"group_pk": self.pk})
# 
class ChatMessage(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete = models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete= models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    view_by_users = models.ManyToManyField(Profile, related_name = "views")
    