from django.contrib import admin
from django.urls import path, include
from TestBarter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('add_product/', views.add_product, name='add_product'),



    path('', include('TestBarter.urls')),
]
