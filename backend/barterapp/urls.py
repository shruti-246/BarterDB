from django.urls import path
from .views import ProductListCreateView, ProductDetailView
from .views import MyProductListView
from .views import RegisterUserView, CustomAuthToken
from .views import TradeCreateView
from .views import MySentTradesView, MyReceivedTradesView
from .views import TradeStatusUpdateView
from django.conf import settings
from django.conf.urls.static import static
from .views import TradeHistoryView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('my-products/', MyProductListView.as_view(), name='my-products'),  # 👈 add this
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('trades/', TradeCreateView.as_view(), name='create-trade'),
    path('my-trades/sent/', MySentTradesView.as_view(), name='my-sent-trades'),
    path('my-trades/received/', MyReceivedTradesView.as_view(), name='my-received-trades'),
    path('trades/<int:pk>/update-status/', TradeStatusUpdateView.as_view(), name='update-trade-status'),
    path('my-trades/history/', TradeHistoryView.as_view(), name='trade-history'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

