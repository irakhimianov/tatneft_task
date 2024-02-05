from typing import Optional

import factory
import faker

fake_ru = faker.Faker('ru_RU')


class Goods(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: fake_ru.word())
    icon = factory.django.ImageField(color='blue')


class User(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: fake_ru.user_name())
    email = factory.Sequence(lambda n: fake_ru.email())
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_superuser = factory.Sequence(lambda n: fake_ru.pybool())

    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)


class Station(factory.django.DjangoModelFactory):
    external_id = factory.Sequence(lambda n: fake_ru.passport_number())
    number = factory.Sequence(lambda n: str(fake_ru.random_int()))
    address = factory.Sequence(lambda n: fake_ru.word())
    coordinates = factory.Sequence(lambda n: [str(coord) for coord in fake_ru.latlng()])

    class Meta:
        model = 'core.Station'
        django_get_or_create = ('external_id',)

    @factory.post_generation
    def fuels(self, create: bool, extracted: Optional[list], **kwargs: dict) -> None:
        if not create:
            return

        if extracted:
            for fuel in extracted:
                self.fuels.add(fuel)
        else:
            self.fuels.add(Fuel())

    @factory.post_generation
    def services(self, create: bool, extracted: Optional[list], **kwargs: dict) -> None:
        if not create:
            return

        if extracted:
            for service in extracted:
                self.services.add(service)
        else:
            self.services.add(Service())


class StationImage(factory.django.DjangoModelFactory):
    station = factory.SubFactory('core.factories.Station')
    url = factory.Sequence(lambda n: fake_ru.image_url())

    class Meta:
        model = 'core.StationImage'


class Fuel(Goods):
    class Meta:
        model = 'core.Fuel'


class Service(Goods):
    class Meta:
        model = 'core.Service'


class FuelStation(factory.django.DjangoModelFactory):
    fuel = factory.SubFactory('core.factories.Fuel')
    station = factory.SubFactory('core.factories.Station')
    price = factory.Sequence(lambda n: fake_ru.pydecimal(right_digits=2, positive=True, min_value=1, max_value=10_000))
    currency = factory.Sequence(lambda n: fake_ru.currency_name())

    class Meta:
        model = 'core.FuelStation'


class ServiceStation(factory.django.DjangoModelFactory):
    service = factory.SubFactory('core.factories.Service')
    station = factory.SubFactory('core.factories.Station')
    price = factory.Sequence(lambda n: fake_ru.pydecimal(right_digits=2, positive=True, min_value=1, max_value=10_000))
    currency = factory.Sequence(lambda n: fake_ru.currency_name())

    class Meta:
        model = 'core.ServiceStation'
