py manage.py test apps.login.tests.func_login_test
py manage.py test apps.registration.tests.func_test_registration
py manage.py test apps.requests.tests.tests_func_request
py manage.py test apps.internalRequests.tests
py manage.py test apps.forms.tests
py manage.py test apps.teams.tests.test_func_teams
py manage.py test apps.teams.tests.test_special
python3 generate_for_test.py
cat tempenv.txt > ../.env
python3 generate.py shell
