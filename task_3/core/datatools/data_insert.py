from django.apps import apps

from core import models


def insert_station_data(
        source_data: list,
        dependency_name: str,
        dependency_model_name: str,
) -> None:
    """
    Сохранение полученных данных со стороннего ресурса в соответствующие модели.
    Для работы со связанными моделями core.FuelStation или core.ServiceStation к core.Station
    :param source_data: Список данных
    :type source_data: list
    :param dependency_name: Имя передаваемой зависимости [`fuels`/`services`]
    :type dependency_name: str
    :param dependency_model_name: Имя модели
    :type dependency_model_name: str
    """
    for data in source_data:
        data = data.get_dict()
        dependencies = data.pop(dependency_name)
        images = data.pop('images', None)

        station, _ = models.Station.objects.get_or_create(**data)
        for dependency in dependencies:
            dependency_data = dependency.get_dict()
            service, _ = models.Service.objects.get_or_create(dependency_data.pop('name'))
            model = apps.get_model(app_label='Core', model_name=dependency_model_name)
            model.objects.get_or_create(station=station, service=service, **dependency_data)

        if images:
            for image_data in images:
                models.StationImage.objects.get_or_create(station=station, url=image_data.url)
