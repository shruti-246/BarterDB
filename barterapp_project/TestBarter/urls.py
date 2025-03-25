from django.urls import path
from TestBarter import views

app_name = 'testbarter'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('add_product/', views.add_product, name='add_product'),
]
