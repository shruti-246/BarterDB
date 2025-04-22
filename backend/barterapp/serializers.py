from rest_framework import serializers
from .models import Product
from django.contrib.auth import get_user_model
from .models import Trade

# 🛍 Product Serializer
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        
# 👤 User Serializer (for registration)
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    items_sold = serializers.SerializerMethodField()
    items_bought = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone_number', 'address', 'items_sold', 'items_bought']

    def get_items_sold(self, user):
        from .models import Trade
        accepted_trades = Trade.objects.filter(offered_by=user, status='accepted')
        return [trade.offered_product.name for trade in accepted_trades]

    def get_items_bought(self, user):
        from .models import Trade
        accepted_trades = Trade.objects.filter(requested_product__owner=user, status='accepted')
        return [trade.requested_product.name for trade in accepted_trades]

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = ['offered_by', 'status', 'created_at']