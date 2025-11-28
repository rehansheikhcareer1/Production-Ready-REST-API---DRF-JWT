from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderCancelView,
    AdminOrderListView
)

urlpatterns = [
    # User order endpoints
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    
    # Admin endpoints
    path('admin/all/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/<int:pk>/update/', OrderUpdateView.as_view(), name='admin-order-update'),
]
