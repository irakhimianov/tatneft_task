from rest_framework import serializers

from core import models


class Fuel(serializers.ModelSerializer):
    class Meta:
        model = models.Fuel
        fields = '__all__'


class Service(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'


class StationList(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(label='Изображения')

    class Meta:
        model = models.Station
        exclude = ('external_id', 'fuels', 'services')

    def get_images(self, obj: models.Station) -> list | None:
        if obj.images.exists():
            return obj.images.values_list('url', flat=True)


class StationRetrieve(StationList):
    fuels = Fuel(label='Топливо', many=True)
    services = Service(label='Дополнительные услуги', many=True)

    class Meta:
        model = models.Station
        exclude = ('external_id',)
