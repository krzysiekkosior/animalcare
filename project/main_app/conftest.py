import pytest
from django.test import Client

from accounts.models import CustomUser
from main_app.models import Case, Comment


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

@pytest.fixture
def adminp():
    adminp = CustomUser.objects.create(
        username='admin',
        email='admin@user.com',
        first_name='Admin_name',
        last_name='Admin_lastname'
    )
    adminp.set_password('pass')
    adminp.is_superuser = True
    adminp.save()
    return adminp

@pytest.fixture
def comment(user, case):
    comment = Comment.objects.create(
        user=user,
        case=case,
        content='Helvetica and Times New Roman walk into a bar. '
                'Get out of here! shouts the bartender. We don’t serve your type.'
    )
    return comment
