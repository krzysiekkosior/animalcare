import pytest
from django.test import Client

from accounts.models import CustomUser


@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    user = CustomUser.objects.create(
        username='user',
        email='useremail@user.com',
        first_name='User_name',
        last_name='User_lastname'
    )
    user.set_password('pass')
    user.save()
    return user
