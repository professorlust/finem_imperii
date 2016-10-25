from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('base.urls', namespace='base'), name='base'),
    url(r'^', include('account.urls', namespace='account'), name='account'),
    url(r'^', include('world.urls', namespace='world'), name='world'),
    url(r'^battle/', include('battle.urls', namespace='battle'), name='battle'),
]
