from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer, 
    OrderCreateSerializer, 
    OrderUpdateSerializer
)
from accounts.permissions import IsAdminUser


class OrderListView(generics.ListAPIView):
    """
    List all orders for current user
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'is_paid']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users see only their orders, admins see all
        if self.request.user.is_admin:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """
    Get detailed order information
    Users can only view their own orders
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only access their own orders
        if self.request.user.is_admin:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(generics.CreateAPIView):
    """
    Create new order
    Authenticated users only
    """
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Return created order with full details
        order_serializer = OrderSerializer(order)
        return Response(
            {
                'message': 'Order placed successfully',
                'order': order_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class OrderUpdateView(generics.UpdateAPIView):
    """
    Update order status
    Admin only
    """
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return updated order
        order_serializer = OrderSerializer(instance)
        return Response({
            'message': 'Order updated successfully',
            'order': order_serializer.data
        })


class OrderCancelView(generics.UpdateAPIView):
    """
    Cancel order
    Users can cancel their own pending orders
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        
        # Only pending orders can be cancelled
        if order.status != 'pending':
            return Response(
                {'error': 'Only pending orders can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update order status
        order.status = 'cancelled'
        order.save()
        
        # Restore product stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        return Response({
            'message': 'Order cancelled successfully',
            'order': OrderSerializer(order).data
        })


class AdminOrderListView(generics.ListAPIView):
    """
    List all orders - Admin only
    With advanced filtering
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'is_paid', 'user']
    search_fields = ['order_number', 'user__email', 'phone']
    ordering_fields = ['created_at', 'total_amount', 'status']
    ordering = ['-created_at']
