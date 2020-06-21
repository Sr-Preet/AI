from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('colorization', views.image, name="color"),
    path('love', views.love, name="love"),
    path('collatz', views.collatz, name='collatz'),
    path('chatbot', views.chat, name='chat'),
    path('chatter', views.chatter, name='chatter'),
    path('soss', views.soss, name='soss'),
]