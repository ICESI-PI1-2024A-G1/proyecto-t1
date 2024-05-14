python3 generate_for_test.py
coverage run manage.py test apps.login.tests.func_login_test
coverage run manage.py test apps.registration.tests.func_test_registration
coverage run manage.py test apps.requests.tests.tests_func_request
coverage run manage.py test apps.internalRequests.tests
coverage run manage.py test apps.forms.tests
coverage run manage.py test apps.teams.tests.test_func_teams
coverage run manage.py test apps.teams.tests.test_special
coverage run manage.py test apps.permissions.tests