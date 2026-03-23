
from django.contrib import admin
from django.urls import include, path
from home.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('accounts/',include('profiles.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]
