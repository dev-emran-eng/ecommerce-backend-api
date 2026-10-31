from rest_framework import viewsets

from .filters import ProductFilter
from .models import Category, Product
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # noqa: RUF012
    search_fields = ['name']  # noqa: RUF012


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]  # noqa: RUF012
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name']  # noqa: RUF012
    ordering_fields = ['price', 'created_at', 'name', 'stock']  # noqa: RUF012

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return qs
        return qs.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])