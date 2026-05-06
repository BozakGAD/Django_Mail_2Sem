from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Почтовый сервер'
admin.site.site_title = 'Администрирование почты'
admin.site.index_title = 'Панель управления'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('actions.urls')),
]
