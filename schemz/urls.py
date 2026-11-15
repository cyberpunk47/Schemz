from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('schemes.urls')),
]

handler404 = 'schemes.views.custom_404'
handler500 = 'schemes.views.custom_500'
