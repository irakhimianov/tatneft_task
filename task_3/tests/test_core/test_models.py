import pytest
from django.contrib.auth.models import User

from core import factories, models


@pytest.mark.django_db
@pytest.mark.parametrize('username', ['test_username1', 'test_username2'])
def test_user_model(username: str) -> None:
    user = factories.User(username=username)
    assert user.username == username
    assert str(user) == user.username
    assert User.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize('external_id', ['id_1', 'id_2'])
def test_station_model(external_id: str) -> None:
    station = factories.Station(external_id=external_id)
    assert station.external_id == external_id
    assert models.Station.objects.count() == 1


@pytest.mark.django_db
def test_station_image_model() -> None:
    factories.StationImage()
    assert models.StationImage.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize('name', ['name_1', 'name_2'])
def test_fuel_model(name: str) -> None:
    fuel = factories.Fuel(name=name)
    assert fuel.name == name
    assert models.Fuel.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize('name', ['name_1', 'name_2'])
def test_service_model(name: str) -> None:
    service = factories.Service(name=name)
    assert service.name == name
    assert models.Service.objects.count() == 1
