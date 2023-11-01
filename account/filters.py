from django_filters import rest_framework as filters


class StoreFilter(filters.FilterSet):
    user = filters.CharFilter(field_name="user__id", lookup_expr="iexact")
