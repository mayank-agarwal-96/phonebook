from django.conf.urls import url
from .views import ContactList

urlpatterns = [
    url(r'^list/', ContactList.as_view(), name='contact-list'),
]