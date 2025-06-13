from django.urls import path, include
from .views import RegistrationView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('registration/', view= RegistrationView.as_view(), name= 'registration'),
    path(route= 'authorization/', view= CustomLoginView.as_view(), name= 'authorization'),
    path("logout/", view = CustomLogoutView.as_view(), name = "logout")
]