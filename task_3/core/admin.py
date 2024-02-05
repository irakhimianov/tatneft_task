from django.contrib import admin
from django.db.models import ImageField

from core import models, widgets


class StationImageInline(admin.StackedInline):
    extra = 0
    model = models.StationImage


class FuelsInline(admin.StackedInline):
    extra = 0
    model = models.Station.fuels.through


class ServicesInline(admin.StackedInline):
    extra = 0
    model = models.Station.services.through


class Goods(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('^name',)
    formfield_overrides = {
        ImageField: {'widget': widgets.AdminImageWidget},
    }


@admin.register(models.Station)
class Station(admin.ModelAdmin):
    inlines = (StationImageInline, FuelsInline, ServicesInline)
    list_display = ('number', 'external_id', 'address', 'coordinates')
    search_fields = ('=external_id', '^number', 'address')


@admin.register(models.Fuel)
class Fuel(Goods):
    ...


@admin.register(models.Service)
class Service(Goods):
    ...


@admin.register(models.FuelStation)
class FuelStation(admin.ModelAdmin):
    list_display = ('fuel', 'station', 'price', 'currency')
    list_filter = ('station', 'fuel', 'currency')
    search_fields = ('station__number', 'fuel__name')


@admin.register(models.ServiceStation)
class ServiceStation(admin.ModelAdmin):
    list_display = ('service', 'station', 'price', 'currency')
    list_filter = ('station', 'service', 'currency')
    search_fields = ('station__number', 'service__name')
