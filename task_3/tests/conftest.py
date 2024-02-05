from typing import Iterator

import pytest
from pytest_django.fixtures import SettingsWrapper
from django.contrib.auth.models import AnonymousUser
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from core import factories

register(factory_class=factories.User, _name='user_factory')
register(factory_class=factories.Station, _name='station_factory')
register(factory_class=factories.StationImage, _name='station_image_factory')
register(factory_class=factories.Fuel, _name='fuel_factory')
register(factory_class=factories.Service, _name='service_factory')
register(factory_class=factories.FuelStation, _name='fuel_station_factory')
register(factory_class=factories.ServiceStation, _name='service_station_factory')


@pytest.fixture(autouse=True)
def _media_root(settings: SettingsWrapper, tmpdir_factory: 'TempdirFactory') -> None:
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True)
def _password_hashers(settings: SettingsWrapper) -> None:
    settings.PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )


@pytest.fixture(autouse=True)
def _auth_backends(settings: SettingsWrapper) -> None:
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )


@pytest.mark.django_db
def personal_token(user: 'User') -> Token:
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.mark.django_db
@pytest.fixture
def superuser() -> 'User':
    return factories.User(is_superuser=True)


@pytest.mark.django_db
@pytest.fixture
def client(superuser: 'User') -> Iterator[APIClient]:
    client = APIClient()
    token = personal_token(user=superuser)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    yield client
    client.force_authenticate(user=AnonymousUser())
