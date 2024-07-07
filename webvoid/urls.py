from django.urls import path
from . import views
from .views import index
from .views import restaurant_list,restaurant_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
]


urlpatterns = [
    path('', views.index, name = 'index'),
    # path('nearby-restaurant_list/', restaurant_list, name='restaurant_list'),
    path('restaurants', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:pk>/', restaurant_detail, name='restaurant_detail'),

    path('menu/', views.menu_detail, name='menu_detail'),
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),


    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

