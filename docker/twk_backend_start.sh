
ls -A /runner

if [ ! -d /runner/code ]; then
    echo "/runner/code do not exist"
    cp -r /code/ /runner/
    cd /runner/code
    bash db_clean_up.sh
    find . -type d -name __pycache__ -exec rm -r {} \+
    python3 manage.py makemigrations
    python3 manage.py migrate --run-syncdb
    python3 gen_fixtures.py st 3
    python3 ./manage.py loaddata output.json
    python3 ./manage.py shell < set_password.py
else
    echo "/runner/code exists"
    cd /runner/code
fi

python3 ./manage.py runserver 0.0.0.0:8000

