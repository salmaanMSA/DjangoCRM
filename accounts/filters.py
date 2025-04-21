import django_filters
from django_filters import DateFilter
from .models import Customer, Product, Tag, Order

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer']