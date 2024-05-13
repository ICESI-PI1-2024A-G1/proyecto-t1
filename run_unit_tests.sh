DESTRUCTIVE=false

coverage erase
coverage run -a manage.py test apps.requests.tests.tests_sharepoint_api
coverage run -a manage.py test utils.testAdmin
coverage run -a manage.py test utils.testModel
coverage run -a manage.py test utils.test
coverage run -a manage.py test apps.permissions.test_unit
coverage run -a manage.py test apps.emailContact.tests
coverage run -a manage.py test apps.login.tests.tests_login
while (( "$#" )); do
  case "$1" in
    --destructive)
      DESTRUCTIVE=true
      shift
      ;;
    *) # Si se encuentra una opción desconocida, imprime un mensaje de error y sale
      echo "Error: Invalid option"
      exit 1
      ;;
  esac
done

if [ "$DESTRUCTIVE" = true ]; then
    coverage run manage.py test apps.login.tests.test_backends
fi
coverage run -a manage.py test apps.registration.tests.tests_registration
coverage run -a manage.py test apps.requests.tests.tests_requests
coverage run -a manage.py test apps.errorHandler.tests
coverage run -a manage.py test apps.teams.tests.tests_teams
coverage run -a manage.py test apps.forms.unit_tests
coverage run -a manage.py test apps.internalRequests.test_unit

coverage report
coverage html
python3 print_results.py