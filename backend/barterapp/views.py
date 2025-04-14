from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Product
from rest_framework.views import APIView
from .serializers import ProductSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from .serializers import TradeSerializer
from django.db.models import Q
from .serializers import UserProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from .models import Trade, QRCode
from .serializers import TradeSerializer
from .models import User, Product, Trade
from .permissions import IsAdminUser

User = get_user_model()

# 🔐 Login View
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

# 🧾 Register View
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

# 🛍 Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class MyProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

class TradeCreateView(generics.CreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(offered_by=self.request.user)

class MySentTradesView(generics.ListAPIView):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(offered_by=self.request.user)


class MyReceivedTradesView(generics.ListAPIView):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(requested_product__owner=self.request.user)

class TradeStatusUpdateView(generics.UpdateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only let owners of the requested product update the status
        return Trade.objects.filter(requested_product__owner=self.request.user)

class TradeHistoryView(generics.ListAPIView):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(
            status="accepted"
        ).filter(
            Q(offered_by=self.request.user) |
            Q(requested_product__owner=self.request.user)
        )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class AdminAllTradesView(ListAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class AdminSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        summary = {
            "total_users": User.objects.count(),
            "total_products": Product.objects.count(),
            "total_trades": Trade.objects.count(),
            "completed_trades": Trade.objects.filter(status='accepted').count()
        }
        return Response(summary)

class QRCodeVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        trade_id = request.data.get("trade_id")

        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response({"error": "Invalid trade ID."}, status=404)

        # Check that trade is accepted
        if trade.status != "accepted":
            return Response({"error": "Trade is not in accepted state."}, status=400)

        # Check if the user is involved in the trade
        if request.user != trade.offered_by and request.user != trade.requested_product.owner:
            return Response({"error": "You are not authorized to verify this trade."}, status=403)

        # Check QR code exists and hasn't been used
        try:
            qr = QRCode.objects.get(trade=trade)
        except QRCode.DoesNotExist:
            return Response({"error": "QR code not found."}, status=404)

        if qr.is_used:
            return Response({"error": "QR code already used."}, status=400)

        # ✅ All good — mark trade as completed and QR as used
        trade.status = "completed"
        trade.save()

        qr.is_used = True
        qr.save()

        return Response({"message": "Trade verified and marked as completed."})