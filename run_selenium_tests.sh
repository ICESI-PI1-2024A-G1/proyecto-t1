python3 generate_for_test.py
coverage run manage.py test apps.login.tests.func_login_test --timing
coverage run manage.py test apps.registration.tests.func_test_registration --timing
coverage run manage.py test apps.requests.tests.tests_func_request --timing
coverage run manage.py test apps.internalRequests.tests --timing
coverage run manage.py test apps.forms.tests --timing
coverage run manage.py test apps.teams.tests.test_func_teams --timing
coverage run manage.py test apps.teams.tests.test_special --timing
coverage run manage.py test apps.permissions.tests --timing