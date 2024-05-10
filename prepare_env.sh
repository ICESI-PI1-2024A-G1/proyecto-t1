pip install -r requirements.txt
npm install
cat .env > tempenv.txt
cat env_test.txt > .env
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 generate_for_test.py shell
python3 manage.py runserver &    