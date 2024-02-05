import logging

from celery import shared_task

from core import datatools

logger = logging.getLogger(__name__)


@shared_task(name='stations_data_receiver')
def get_stations_data() -> None:
    """
    Задача для выполнения запроса в сторонний источник,
    содержащий информацию по каждой из АЗС
    """
    stations_data = datatools.DataReceiver().get_stations_data()
    if not stations_data:
        return

    try:
        datatools.insert_station_data(
            source_data=stations_data,
            dependency_name='services',
            dependency_model_name='ServiceStation',
        )
    except Exception as e:
        logger.error(f'Ошибка: {e}')


@shared_task(name='station_fuels_receiver')
def get_station_fuels_data() -> None:
    """
    Задача для выполнения запроса в сторонний источник,
    содержащий информацию по топливу в АЗС
    """
    station_fuels_data = datatools.DataReceiver().get_station_fuels_data()
    if not station_fuels_data:
        return

    try:
        datatools.insert_station_data(
            source_data=station_fuels_data,
            dependency_name='fuels',
            dependency_model_name='FuelStation',
        )
    except Exception as e:
        logger.error(f'Ошибка: {e}')
