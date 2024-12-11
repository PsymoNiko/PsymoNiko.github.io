from django_filters import rest_framework as filters
from .models import Transaction


class TransactionFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    date_range = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Transaction
        fields = ['receiver', 'status', 'min_amount', 'max_amount', 'date_range']
