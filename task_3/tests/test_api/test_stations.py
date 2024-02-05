import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core import factories, models


@pytest.mark.django_db
def test_stations_list(client: APIClient) -> None:
    url = 'api:v1:stations-list'
    factories.Station()
    response = client.get(reverse(url))

    assert response.status_code == 200
    assert response.data.get('count') == models.Station.objects.count()


@pytest.mark.django_db
def test_stations_detail(client: APIClient) -> None:
    url = 'api:v1:stations-detail'
    station = factories.Station()
    response = client.get(reverse(url, kwargs={'pk': station.pk}))

    assert response.status_code == 200
    assert response.data.get('number') == station.number