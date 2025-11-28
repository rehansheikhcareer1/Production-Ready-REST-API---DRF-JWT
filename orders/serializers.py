from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer
import random
import string


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for order items
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 
                  'quantity', 'price', 'subtotal']
        read_only_fields = ['price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """
    Detailed order serializer with all items
    """
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'user_email', 
                  'shipping_address', 'shipping_city', 'shipping_state', 
                  'shipping_pincode', 'phone', 'status', 'payment_method', 
                  'is_paid', 'total_amount', 'total_items', 'items',
                  'created_at', 'updated_at', 'delivered_at']
        read_only_fields = ['order_number', 'user', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new orders
    """
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'shipping_city', 'shipping_state', 
                  'shipping_pincode', 'phone', 'payment_method', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Generate unique order number
        order_number = 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        # Calculate total amount
        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            # Use product's current price
            price = product.final_price
            total += price * quantity
        
        # Create order
        order = Order.objects.create(
            order_number=order_number,
            user=self.context['request'].user,
            total_amount=total,
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.final_price
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            
            # Update product stock
            product.stock -= quantity
            product.save()
        
        return order
    
    def validate_items(self, items):
        """Validate order items"""
        if not items:
            raise serializers.ValidationError("Order must contain at least one item")
        
        for item in items:
            product = item['product']
            quantity = item['quantity']
            
            # Check if product is available
            if not product.is_available:
                raise serializers.ValidationError(f"{product.name} is not available")
            
            # Check stock
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Only {product.stock} units of {product.name} available"
                )
        
        return items


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating order status
    Admin/Vendor only
    """
    class Meta:
        model = Order
        fields = ['status', 'is_paid']
