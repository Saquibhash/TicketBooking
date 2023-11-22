
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
run mailhog
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

-------------------------------------------------------------
manager-
manager@bms.com
MANAGER

customer
Saquib@gmail.com
abcd
