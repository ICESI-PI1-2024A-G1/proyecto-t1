coverage erase
coverage run manage.py test apps.login.tests.tests_login
coverage run manage.py test apps.registration.tests.tests_registration
coverage run manage.py test apps.requests.tests.tests_requests
coverage run manage.py test apps.login.tests.func_login_test
coverage run manage.py test apps.registration.tests.func_test_registration
coverage run manage.py test apps.requests.tests.tests_func_request
coverage run manage.py test apps.internalRequests.tests
coverage run manage.py test apps.forms.tests
coverage run manage.py test apps.permissions.tests
coverage run manage.py test apps.teams.tests.test_func_teams
coverage run manage.py test apps.teams.tests.test_special
py generate_for_test.py
py generate.py shell
coverage report
py print_results.py