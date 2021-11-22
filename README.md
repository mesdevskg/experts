# Randomly pick Experts
This project made for 'Okuu Kitebi' organization by 'Jani Kitep' Organization.

git

    git clone git@github.com:Soyuzbek/experts.git
    
Database
   
    sudo apt install postgresql
    sudo -su postgres psql
    CREATE DATABASE <db_name>;
    CREATE ROLE <role> WITH PASSWORD <pwd>;
    ALTER ROLE <role> SET CLIENT_ENCODING TO 'utf8';
    ALTER ROLE <role> SET DEFAULT_TRANSACTION_ISOLATION TO 'read committed';
    ALTER ROLE <role> SET TIMEZONE TO 'Asia/Bishkek';
    GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <role>

Virtualenv
    
    sudo apt install python3-pip
    pip3 install pipenv
    pipenv install
    pipenv shell
Django
    
    python manage.py migrate
    python manage.py dumpdata --natural-primary --exclude=contenttypes --exclude=auth --exclude=admin.logentry --exclude=sessions.session --indent 4 > ../upai.json 
    python manage.py loaddata data.json
    python manage.py runserver

