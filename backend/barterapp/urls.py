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
from .views import ProfileView
from .views import AdminAllTradesView
from .views import AdminSummaryView
from .views import QRCodeVerificationView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('my-products/', MyProductListView.as_view(), name='my-products'),  
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('trades/', TradeCreateView.as_view(), name='create-trade'),
    path('my-trades/sent/', MySentTradesView.as_view(), name='my-sent-trades'),
    path('my-trades/received/', MyReceivedTradesView.as_view(), name='my-received-trades'),
    path('trades/<int:pk>/update-status/', TradeStatusUpdateView.as_view(), name='update-trade-status'),
    path('my-trades/history/', TradeHistoryView.as_view(), name='trade-history'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('admin-only/trades/', AdminAllTradesView.as_view(), name='admin-all-trades'),
    path('admin-only/summary/', AdminSummaryView.as_view(), name='admin-summary'),
    path('trades/verify-qr/', QRCodeVerificationView.as_view(), name='verify-qr'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

