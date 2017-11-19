from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from decorators import inchar_required
from character.views import create, CharacterCreationView, \
    activate, pause, unpause, character_home, \
    TravelView, travel_view_iframe, public_order, character_view, \
    character_view_iframe, InventoryView, transfer_cash

urlpatterns = [
    url(r'^create$', create, name='create'),
    url(r'^create/(?P<world_id>[0-9]+)$', login_required(CharacterCreationView.as_view()), name='create'),
    url(r'^activate/(?P<char_id>[0-9]+)$', activate, name='activate'),
    url(r'^pause$', pause, name='pause'),
    url(r'^unpause$', unpause, name='unpause'),
    url(r'^home$', character_home, name='character_home'),
    url(r'^travel/(?P<settlement_id>[0-9]+)?$', inchar_required(TravelView.as_view()), name='travel'),
    url(r'^travel_iframe/(?P<settlement_id>[0-9]+)?$', travel_view_iframe, name='travel_iframe'),
    url(r'^inventory$', inchar_required(InventoryView.as_view()), name='inventory'),
    url(r'^view/(?P<character_id>[0-9]+)$', character_view, name='character'),
    url(r'^view_iframe/(?P<character_id>[0-9]+)$', character_view_iframe, name='character_iframe'),
    url(r'^public_order$', public_order, name='public_order'),
    url(r'^transfer_cash$', transfer_cash, name='transfer_cash'),
]
