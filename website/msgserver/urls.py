from django.urls import path
from . import views


urlpatterns = [
    path('', views.showall, name='messages'),
    path('get/<str:key>/', views.messages, name='message'),
    path('create/', views.createMessage, name='create'),
    path('update/<str:key>/', views.updateMessage, name='update')
]
