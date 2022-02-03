import pytest

from main_app.models import Case, Comment


@pytest.mark.django_db
def test_landing_page_url(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_profile_url(client, user):
    client.login(username='user', password='pass')
    response = client.get('/accounts/profile/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_case_url(client):
    response = client.get('/add-case/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_case(client):
    pre_add_cases_amount = Case.objects.count()
    context = {
        'type': '0',
        'place': 'place',
        'description': 'description'
    }
    client.post('/add-case/', context)
    after_add_cases_amount = Case.objects.count()
    assert after_add_cases_amount == pre_add_cases_amount + 1


@pytest.mark.django_db
def test_close_case_as_user(client, user, case):
    client.login(username='user', password='pass')
    response = client.get(f'/case/{case.pk}/close/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_close_case_as_admin(client, adminp, case):
    client.login(username='admin', password='pass')
    response = client.get(f'/case/{case.pk}/close/')
    assert response.status_code == 302
    case.refresh_from_db()
    assert case.status == 1


@pytest.mark.django_db
def test_delete_case_as_user(client, user, case):
    client.login(username='user', password='pass')
    response = client.get(f'/case/{case.pk}/delete/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_case_as_admin(client, adminp, case):
    client.login(username='admin', password='pass')
    cases = Case.objects.count()
    response = client.get(f'/case/{case.pk}/delete/')
    assert response.status_code == 302
    assert Case.objects.count() == cases - 1


@pytest.mark.django_db
def test_add_comment(client, user, case):
    pre_add_comments_amount = Comment.objects.count()
    client.login(username='user', password='pass')
    context = {
        'content': 'Treść komentarza'
    }
    client.post(f'/case/{case.pk}/comment/', context)
    after_add_comments_amount = Comment.objects.count()
    assert after_add_comments_amount == pre_add_comments_amount + 1
