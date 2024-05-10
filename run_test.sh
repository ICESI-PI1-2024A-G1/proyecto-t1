coverage erase
py manage.py test utils.testAdmin
py manage.py test utils.testModel
py manage.py test utils.test
coverage run manage.py test apps.login.tests.tests_login
coverage run manage.py test apps.registration.tests.tests_registration
coverage run manage.py test apps.requests.tests.tests_requests
coverage run manage.py test apps.login.tests.func_login_test
coverage run manage.py test apps.registration.tests.func_test_registration
coverage run manage.py test apps.requests.tests.tests_func_request
coverage run manage.py test apps.internalRequests.tests
coverage run manage.py test apps.forms.tests
coverage run manage.py test apps.teams.tests.test_func_teams
coverage run manage.py test apps.teams.tests.test_special
python3 generate_for_test.py
coverage run manage.py test apps.permissions.tests
python3 generate.py shell
coverage report
python3 print_results.py