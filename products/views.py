from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ProductListSerializer,
    ProductCreateUpdateSerializer,
    ReviewSerializer
)
from accounts.permissions import IsVendorOrAdmin, IsAdminUser


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create new one
    GET: Anyone can view
    POST: Admin only
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    def perform_create(self, serializer):
        # Only admin can create categories
        if not self.request.user.is_admin:
            return Response(
                {'error': 'Only admin can create categories'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category
    Admin only for update/delete
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        if not self.request.user.is_admin:
            return Response(
                {'error': 'Only admin can update categories'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        if not self.request.user.is_admin:
            return Response(
                {'error': 'Only admin can delete categories'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class ProductListView(generics.ListAPIView):
    """
    List all products with filtering, search and pagination
    Public endpoint - anyone can view
    """
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'vendor', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'views']
    ordering = ['-created_at']  # Default ordering


class ProductDetailView(generics.RetrieveAPIView):
    """
    Get detailed product information
    Increments view count on each access
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductCreateView(generics.CreateAPIView):
    """
    Create new product
    Only vendors and admins can create products
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsVendorOrAdmin]
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


class ProductUpdateView(generics.UpdateAPIView):
    """
    Update product
    Only product owner (vendor) or admin can update
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def perform_update(self, serializer):
        product = self.get_object()
        # Check if user is owner or admin
        if product.vendor != self.request.user and not self.request.user.is_admin:
            return Response(
                {'error': 'You do not have permission to update this product'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()


class ProductDeleteView(generics.DestroyAPIView):
    """
    Delete product
    Only product owner or admin can delete
    """
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def perform_destroy(self, instance):
        # Check permissions
        if instance.vendor != self.request.user and not self.request.user.is_admin:
            return Response(
                {'error': 'You do not have permission to delete this product'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class MyProductsView(generics.ListAPIView):
    """
    List products created by current vendor
    """
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated, IsVendorOrAdmin]
    
    def get_queryset(self):
        # Return only products created by current user
        return Product.objects.filter(vendor=self.request.user)


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    List reviews for a product or create new review
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id)
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(user=self.request.user, product_id=product_id)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a review
    Only review owner can update/delete
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            return Response(
                {'error': 'You can only update your own reviews'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user and not self.request.user.is_admin:
            return Response(
                {'error': 'You can only delete your own reviews'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
