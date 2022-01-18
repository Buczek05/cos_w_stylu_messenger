from django.urls import path
from . import views

app_name = 'message'

urlpatterns = [
    path('create', views.Message_Create.as_view(), name='create'),
    path('view/<int:pk>', views.Message_user_view.as_view(), name='view'),
]