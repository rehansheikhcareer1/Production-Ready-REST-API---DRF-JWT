from rest_framework import serializers
from .models import Category, Product, ProductImage, Review
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'is_active', 
                  'created_at', 'product_count']
    
    def get_product_count(self, obj):
        """Get total products in this category"""
        return obj.products.filter(is_available=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for additional product images
    """
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for product reviews
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'user_id', 'rating', 'comment', 
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set user from request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """
    Detailed product serializer with all related data
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.username', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category', 'category_name',
                  'price', 'discount_price', 'final_price', 'stock', 'is_available',
                  'image', 'images', 'vendor', 'vendor_name', 'views', 
                  'reviews', 'average_rating', 'review_count',
                  'created_at', 'updated_at']
        read_only_fields = ['views', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        """Calculate average rating from reviews"""
        reviews = obj.reviews.all()
        if reviews:
            total = sum([review.rating for review in reviews])
            return round(total / len(reviews), 1)
        return 0
    
    def get_review_count(self, obj):
        """Get total number of reviews"""
        return obj.reviews.count()


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product listing
    Used in list views for better performance
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    vendor_name = serializers.CharField(source='vendor.username', read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category_name', 'price', 
                  'discount_price', 'final_price', 'stock', 'is_available',
                  'image', 'vendor_name', 'average_rating', 'created_at']
    
    def get_average_rating(self, obj):
        """Calculate average rating"""
        reviews = obj.reviews.all()
        if reviews:
            total = sum([review.rating for review in reviews])
            return round(total / len(reviews), 1)
        return 0


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating products
    """
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'category', 'price', 
                  'discount_price', 'stock', 'is_available', 'image']
    
    def create(self, validated_data):
        # Set vendor from request user
        validated_data['vendor'] = self.context['request'].user
        return super().create(validated_data)
