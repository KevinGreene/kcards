# pylint: disable=redefined-outer-name

import pytest
from freezegun import freeze_time

from kcards.app import create_app
from kcards.settings import get_config
from kcards.models import Room, Color


@pytest.fixture
def app():
    return create_app(get_config('test'))


@pytest.fixture
def client(app):
    Room.objects.delete()
    return app.test_client()


@pytest.fixture
@freeze_time("2016-11-09 9:33:12")
def room():
    room = Room(code='foobar')
    room.save()
    return room


@pytest.fixture
def populated_room(room):
    room.add_card("John Doe", Color.green)
    room.add_card("Bob Smith", Color.yellow)
    room.add_card("Dan Lindeman", Color.green)
    room.add_card("Jace Browning", Color.red)
    room.save()
    return room
