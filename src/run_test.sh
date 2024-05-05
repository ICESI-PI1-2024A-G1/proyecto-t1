py manage.py test apps.login.tests.func_login_test
py manage.py test apps.registration.tests.func_test_registration
py manage.py test apps.requests.tests.tests_func_request
py manage.py test apps.internalRequests.tests
py manage.py test apps.forms.tests
cat tempenv.txt > ../.env
python3 generate.py shell
