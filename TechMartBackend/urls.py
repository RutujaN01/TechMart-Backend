"""
URL configuration for TechMartBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls

from demo import urls as demo_urls
from users import urls as users_urls
from items import urls as items_urls
from wishlists import urls as wishlist_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include(oauth2_urls)),
    path('demo/', include(demo_urls)),
    path('items/', include(items_urls)),
    path('users/', include(users_urls)),
    path('wishlists/', include(wishlist_urls)),
]
