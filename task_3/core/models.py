from django.core.validators import MinValueValidator
from django.db import models


class Goods(models.Model):
    name = models.CharField('наименование', max_length=255, db_index=True)
    icon = models.ImageField('иконка', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.name)


class Station(models.Model):
    external_id = models.CharField('внешний идентификатор', max_length=255, db_index=True)
    number = models.CharField('номер', max_length=255, blank=True, db_index=True)
    address = models.TextField('адрес', blank=True)
    coordinates = models.CharField('координаты', max_length=255, blank=True)
    fuels = models.ManyToManyField('core.Fuel', blank=True, through='core.FuelStation')
    services = models.ManyToManyField('core.Service', blank=True, through='core.ServiceStation')

    created_at = models.DateTimeField('когда создан', auto_now_add=True)
    updated_at = models.DateTimeField('когда обновлен', auto_now=True)

    class Meta:
        verbose_name = 'заправочная станция'
        verbose_name_plural = 'заправочные станции'
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return str(self.number)


class StationImage(models.Model):
    station = models.ForeignKey(
        'core.Station',
        verbose_name='заправочная станция',
        on_delete=models.CASCADE,
        related_name='images',
    )
    url = models.URLField('ссылка на изображение', max_length=512)

    class Meta:
        verbose_name = 'изображение заправочной станции'
        verbose_name_plural = 'изображения заправочных станций'

    def __str__(self) -> str:
        return str(self.station)


class Fuel(Goods):
    class Meta:
        verbose_name = 'топливо'
        verbose_name_plural = 'топливо'


class Service(Goods):
    class Meta:
        verbose_name = 'дополнительная услуга'
        verbose_name_plural = 'дополнительные услуги'


class FuelStation(models.Model):
    fuel = models.ForeignKey(
        'core.Fuel',
        verbose_name='топливо',
        on_delete=models.CASCADE,
        related_name='fuel_stations',
    )
    station = models.ForeignKey(
        'core.Station',
        verbose_name='заправочная станция',
        on_delete=models.CASCADE,
        related_name='fuel_stations',
    )
    price = models.DecimalField('цена', default=0, max_digits=100, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField('валюта', max_length=255, blank=True, db_index=True)

    class Meta:
        verbose_name = 'топливо в станции'
        verbose_name_plural = 'топливо в станции'

    def __str__(self) -> str:
        return str(self.station)


class ServiceStation(models.Model):
    service = models.ForeignKey(
        'core.Service',
        verbose_name='дополнительная услуга',
        on_delete=models.CASCADE,
        related_name='service_stations',
    )
    station = models.ForeignKey(
        'core.Station',
        verbose_name='заправочная станция',
        on_delete=models.CASCADE,
        related_name='service_stations',
    )
    price = models.DecimalField('цена', default=0, max_digits=100, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField('валюта', max_length=255, db_index=True)

    class Meta:
        verbose_name = 'дополнительная услуга в станции'
        verbose_name_plural = 'дополнительные услуги в станции'

    def __str__(self) -> str:
        return str(self.station)
