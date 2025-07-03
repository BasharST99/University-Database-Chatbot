from django.contrib import admin
from django.urls import path
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ask/', views.ask_question, name='ask_question'),
]