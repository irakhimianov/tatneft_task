import logging
import json
from dataclasses import dataclass, asdict

import requests
from constance import config

logger = logging.getLogger(__name__)


@dataclass
class Goods:
    name: str
    price: str
    currency: str


@dataclass
class Stations:
    id: str
    number: str
    coordinates: list
    address: str
    images: list[str]
    services: list[Goods] | list[dict]

    def __post_init__(self) -> None:
        self.services = [Goods(**s) for s in self.services if isinstance(s, dict)]

    def get_dict(self) -> dict:
        data = asdict(self)
        data['external_id'] = data.pop('id')
        return data


@dataclass
class StationFuels:
    id: str
    fuels: list[Goods] | list[dict]

    def __post_init__(self) -> None:
        self.fuels = [Goods(**s) for s in self.fuels if isinstance(s, dict)]

    def get_dict(self) -> dict:
        data = asdict(self)
        data['external_id'] = data.pop('id')
        return data


class DataReceiver:
    def get_stations_data(self) -> list[Stations] | None:
        """
        Запрос в сторонний ресурс источника данных
        :return: Данные со стороннего ресурса
        :rtype: list[Stations], optional
        """
        response = self._request(url=config.SOURCE_1, method='get')
        if data := response.get('data'):
            return [Stations(**data)]

    def get_station_fuels_data(self) -> list[StationFuels] | None:
        """
        Запрос в сторонний ресурс источника данных
        :return: Данные со стороннего ресурса
        :rtype: list[StationFuels], optional
        """
        response = self._request(url=config.SOURCE_2, method='get')
        if data := response.get('data'):
            return [StationFuels(**data)]

    @property
    def allowed_methods(self) -> tuple[str, str]:
        return 'get', 'post'

    def _request(self, url: str, method: str, data: dict = None) -> dict | None:
        """
        Реализация запроса в сторонний ресурс источника данных
        :param url: Ссылка для осуществления запроса
        :type url: str
        :param method: Http-метод для осуществления запроса
        :type method: str
        :param data: Дополнительные данные, передаваемые в заголовке, либо в теле, для осуществления запроса
        :type data: dict, optional
        :return: Данные со стороннего ресурса в формате `{status: 200, data={...}}
        :rtype: dict, optional
        """
        if method not in self.allowed_methods:
            logger.error(f'Неподдерживаемый метод {method = }!')
            return

        json_param = {'post': 'data', 'get': 'params'}
        opts = {'url': url}
        if data:
            opts |= {json_param.get(method): data}

        logger.info(f'{method.upper()} request to {url} with {opts = }')
        try:
            response = getattr(requests, method)(**opts)
            if response.status_code == 200:
                return {'status': response.status_code, 'data': json.loads(response.content)}
            return {'status': response.status_code}
        except Exception as e:
            logger.error(f'Ошибка во время выполнения запроса: {e}')
