from typing import Type

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.serializers import Serializer

from api.v1 import filters, serializers
from core import models


class Station(ReadOnlyModelViewSet):
    queryset = models.Station.objects.all()
    filterset_class = filters.Station

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ('list',):
            return serializers.StationList
        return serializers.StationRetrieve
