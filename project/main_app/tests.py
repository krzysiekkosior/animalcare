import pytest

@pytest.mark.django_db
def test_landing_page_url(client):
    response = client.get('/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_profile_url(client, user):
    client.login(username='user', password='pass')
    response = client.get('/accounts/profile/')
    assert response.status_code == 200
