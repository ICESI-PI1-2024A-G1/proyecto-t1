pip install -r requirements.txt
cat .env > tempenv.txt
cat env_test.txt > .env
rm db.sqlite3
py manage.py makemigrations
py manage.py migrate
py generate_for_test.py shell
py manage.py runserver &    