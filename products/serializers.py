from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'created_at')
        read_only_fields = ('slug', 'created_at')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'category_name', 'name', 'slug', 'description',
            'price', 'stock', 'is_active', 'created_at', 'updated_at',
        )
        read_only_fields = ('slug', 'created_at', 'updated_at')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0.')
        return value