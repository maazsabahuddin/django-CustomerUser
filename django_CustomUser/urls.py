
from django.contrib import admin
from django.urls import path
from User.views import Register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', Register.as_view(), name='user_register_api'),
]
