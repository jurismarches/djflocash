from django.conf.urls import url

from .views import NotificationReceive


urlpatterns = [
    url(r'^notification/$', NotificationReceive.as_view(), name='notification_receive'),
]
