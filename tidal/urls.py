from django.conf.urls import include, url
from django.contrib import admin

from hydro.views import hydro_view, hydro_JSON_data_update

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hydro/', hydro_view, name="hydro"),
    url(r'^updateJSON/$', hydro_JSON_data_update, name="hydroJSON"),
]
