import pytest

from pytest_django.fixtures import _django_db_fixture_helper


@pytest.fixture(scope='session', autouse=True)
def db_session(request, django_db_setup, django_db_blocker):
    """
    Changed scope to 'session'
    """
    if 'django_db_reset_sequences' in request.funcargnames:
        request.getfixturevalue('django_db_reset_sequences')
    if 'transactional_db' in request.funcargnames \
            or 'live_server' in request.funcargnames:
        request.getfixturevalue('transactional_db')
    else:
        _django_db_fixture_helper(request, django_db_blocker, transactional=False)


@pytest.fixture(scope='session', autouse=True)
def prepare_db():
    # call_command('loaddata', 'rates.json')
    pass
