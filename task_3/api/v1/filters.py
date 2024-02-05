from django_filters import rest_framework as filters

from core import models


class Station(filters.FilterSet):
    number = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = models.Station
        fields = ('external_id', 'number', 'address')
