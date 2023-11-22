from flask import Flask, render_template, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .db import db as db_instance
from . import worker
from . import config
from . import tasks
import os
from redis import Redis
from .cache import cache

db = db_instance.database

bcrypt = Bcrypt()


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.config['JWT_SECRET_KEY'] = 'hpMWF35LvhMs9k2ZJETFqL69UlW3EWTM41wxggED'
    jwt = JWTManager(app)
    
    cache.init_app(app)

    app.config.from_object(config)

    app.config["SECRET_KEY"] = b'&\xab\x84$\xa5\t\x00Zs\x96\xcf\xaa\xf2\xd3\xebZ'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
   
    db.init_app(app)
    worker.create_celery_app(app)
  

    login_manager = LoginManager()
    login_manager.init_app(app) 
    from . import model
    @login_manager.user_loader
    def load_user(user_id):
        return model.User.query.get(int(user_id))
    
    from . import main
    from . import authenticate
    from . import manager
    app.register_blueprint(main.blue)
    app.register_blueprint(authenticate.blue)
    app.register_blueprint(manager.blue)

    # Register the export_venue_csv route after registering the blueprints
    from .main import export_venue_csv
    app.add_url_rule('/export_venue_csv/<int:selected_venue_id>', 'export_venue_csv_route', export_venue_csv)

    with app.app_context():
        db.create_all()
        db.session.commit()
    
    return app


# def create_app(test_config=None):
#     app = Flask(__name__)
#     CORS(app)
#     app.config['JWT_SECRET_KEY'] = 'hpMWF35LvhMs9k2ZJETFqL69UlW3EWTM41wxggED'
#     jwt = JWTManager(app)

#     app.config.from_object(config)

#     app.config["SECRET_KEY"] = b'&\xab\x84$\xa5\t\x00Zs\x96\xcf\xaa\xf2\xd3\xebZ'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#     app.config.from_mapping(
#         CELERY=dict(
#             broker_url="redis://localhost:6379/1",
#             result_backend="redis://localhost:6379/2",
#             task_ignore_result=True,
#         ),
#     )
   

#     db.init_app(app)
#     worker.create_celery_app(app)

#     login_manager = LoginManager()
#     login_manager.init_app(app) 
#     from . import model
#     @login_manager.user_loader
#     def load_user(user_id):
#         return model.User.query.get(int(user_id))
    

    
#     from . import main
#     from . import authenticate
#     from . import manager
#     app.register_blueprint(main.blue)
#     app.register_blueprint(authenticate.blue)
#     app.register_blueprint(manager.blue)

#     with app.app_context():
#         db.create_all()
#         db.session.commit()
    
#     return app



# print('creating app')
# # create app
# app = create_app()
# celery = app.extensions["celery"]

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, tasks.send_email.s())
#     # sender.add_periodic_task(10.0, tasks.senddm.s())
#     # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

# @celery.task
# def test(arg):
#     print(arg)