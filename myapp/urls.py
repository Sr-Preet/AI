from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('colorization', views.image, name="color"),
    path('love', views.love, name="love"),
    path('collatz', views.collatz, name='collatz'),
]