from django.urls import path
from message import views

app_name = 'message'

urlpatterns = [
    path('', views.Message_user_view.as_view(), name='view'),
    path('<int:pk>', views.Message_user_view.as_view(), name='view_pk'),
    path('send_js/<int:pk>', views.Create_message_js.as_view(), name='send_js'),
    path('check_js/<int:pk>', views.check_message_js.as_view(), name='check_js'),
    path('add_previous_js/<int:pk>/<int:last>', views.previous_add_js.as_view(), name='add_previous'),
]
