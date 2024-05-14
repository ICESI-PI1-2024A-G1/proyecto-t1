DESTRUCTIVE=false

coverage erase
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
coverage run -a manage.py test apps.requests.tests.tests_sharepoint_api  --timing
coverage run -a manage.py test utils.testAdmin --timing
coverage run -a manage.py test utils.testModel --timing
coverage run -a manage.py test utils.test --timing
coverage run -a manage.py test apps.permissions.test_unit --timing
coverage run -a manage.py test apps.emailContact.tests --timing
coverage run -a manage.py test apps.login.tests.tests_login --timing
coverage run -a manage.py test apps.registration.tests.tests_registration --timing
coverage run -a manage.py test apps.requests.tests.tests_requests --timing
coverage run -a manage.py test apps.errorHandler.tests --timing
coverage run -a manage.py test apps.teams.tests.tests_teams --timing
coverage run -a manage.py test apps.forms.unit_tests --timing
coverage run -a manage.py test apps.notifications.tests --timing
coverage run -a manage.py test apps.internalRequests.test_unit --timing
coverage run -a manage.py test apps.permissions.unit_tests --timing

coverage report
coverage html
python3 print_results.py