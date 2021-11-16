import pytest
from django.test import Client

from accounts.models import CustomUser
from main_app.models import Case


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

@pytest.fixture
def case(user):
    case = Case.objects.create(
        user=user,
        type=0,
        place='next to Lorem Ipsum',
        description='big, dappled cow',
    )
    return case
