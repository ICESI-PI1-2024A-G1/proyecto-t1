pip install -r requirements.txt
cat .env > tempenv.txt
cat env_test.txt > .env
python3 manage.py makemigrations
rm db.sqlite3
python3 manage.py migrate
python3 generate_for_test.py shell
python3 manage.py runserver &   