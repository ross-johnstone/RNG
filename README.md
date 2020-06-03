# RNG

A web application allowing users to rate and discuss relatively new games.

## PythonAnywhere

http://ratenewgameswad2.pythonanywhere.com/rng/


## Running Instructions

git clone https://github.com/ross-johnstone/RNG.git

pip install -r requirements.txt

cd wad_project

git manage.py makemigrations

git manage.py migrate

git manage.py migrate --run-syncdb

git populate_rng.py 

git manage.py runserver
