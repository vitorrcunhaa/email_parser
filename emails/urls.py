from django.urls import path
from . import views

urlpatterns = [
    path('', views.email_list, name='email_list'),
    path('email/<int:pk>/', views.email_detail, name='email_detail'),
    path('email/new/', views.email_create, name='email_create'),
    path('email/<int:pk>/edit/', views.email_update, name='email_update'),
    path('email/<int:pk>/delete/', views.email_delete, name='email_delete'),
]