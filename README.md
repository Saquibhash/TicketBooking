# Ticket Booking (ticket show) app using flask and vuejs
This is a ticket booking app similar to book my show i made using flask and vuejs for front end, sqlite for db and also has a monthly and daily scheduled task setup through celery and redis server.
 this was for my app dev-2 project.
I have attached the problem statement as well along with the files. kindly check that for other specific requiremnets followed.

all copyrights remains to me
Kindly use for reference.

you will be needing 6 terminals
1 backend, 2 frontend, 3. redis server, 4. mailhog server, 5. clerey worker, 6. celery beat

Create an environment in ticket-main

python3 -m venv virtual
. virtual/bin/activate


Install the requirements

pip install -U pip
pip install Flask python-dateutil
pip install flask-sqlalchemy mysqlclient
pip install flask-bcrypt
pip install flask-login
pip install flask-cors
pip install flask_jwt_extended
pip install marshmallow
pip install celery
pip install redis
pip install flask_caching

---------------------------------------------

for backend


go to backend folder

Run the app
flask --app=ticket run

----------------------------------------------------

for frontend

run virtual env in ticket-main

go to frontend folder

npm install
```

### Compile and Hot-Reload for Development


npm run dev


--------------------------------------------------------------


run redis server

redis-server

in case redis server is busy
 sudo /etc/init.d/redis-server stop
 ps aux | grep redis-server
 
 
 -------------------------------------------------
run mailhog (install first)
~/go/bin/MailHog


----------------------------------------------------------
activate virtual in ticket-main

go to backend

Worker:
celery -A ticket.cell.cel_app worker -l INFO

------------------------------------------------------------

activate virtual in ticket-main

go to backend

Beat:
celery -A ticket.cell.cel_app beat -l INFO

