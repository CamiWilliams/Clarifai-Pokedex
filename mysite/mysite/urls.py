from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import pokemon.views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', pokemon.views.LandingPageView.as_view(), name='index'),
    url(r'^result/', pokemon.views.ResultPageView.as_view(), name='result'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
