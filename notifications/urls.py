from django.urls import path
from .views import ListNotifications


urlpatterns = [
    path('', ListNotifications.as_view(), name='list_notifications')
]