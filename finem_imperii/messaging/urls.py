from django.conf.urls import url

from decorators import inchar_required
from messaging.views import mark_all_read, messages_list, home, mark_read, mark_favourite, favourites_list, \
    sent_list, add_contact, remove_contact, ComposeView, reply

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^read/(?P<recipient_id>[0-9]+)$', mark_read, name='mark_read'),
    url(r'^favourite/(?P<recipient_id>[0-9]+)$', mark_favourite, name='mark_favourite'),
    url(r'^read_all$', mark_all_read, name='mark_all_read'),
    url(r'^all$', messages_list, name='messages_list'),
    url(r'^favourites$', favourites_list, name='favourites'),
    url(r'^sent', sent_list, name='sent'),
    url(r'^compose$', inchar_required(ComposeView.as_view()), name='compose'),
    url(r'^compose/character/(?P<character_id>[0-9]+)$', inchar_required(ComposeView.as_view()), name='compose_character'),
    url(r'^reply/(?P<recipient_id>[0-9]+)$', reply, name='reply'),
    url(r'^favourite/character/(?P<character_id>[0-9]+)$', add_contact, name='add_contact'),
    url(r'^unfavourite/character/(?P<character_id>[0-9]+)$', remove_contact, name='remove_contact'),
]
