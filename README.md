# RNG

A web application allowing users to rate and discuss relatively new games.


## Team Members

Jason Cook(2328261c) Alasdair Russel(2315645r) Ross Johnstone(2326663j) Jamie Allan(2316615a) Liam Brodie(2315645r)

## PythonAnywhere

http://ratenewgameswad2.pythonanywhere.com/rng/


## Running Instructions

git clone https://github.com/JAA1999/WAD_Project.git

pip install -r requirements.txt

cd wad_project

git manage.py makemigrations

git manage.py migrate

git manage.py migrate --run-syncdb

git populate_rng.py 

git manage.py runserver
