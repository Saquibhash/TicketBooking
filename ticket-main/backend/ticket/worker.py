from celery import Task, Celery

cel = Celery ()
cel.config_from_object("ticket.celeryconfig")
    
def create_celery_app(app):    
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
        
    print('reading context: ', app.name)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object("ticket.celeryconfig")
    celery_app.set_default()
    # app.extensions["celery"] = celery_app
    return celery_app

class AppContextTask(Task):
  def __call__(self,*args,**kwargs):
    with self.app.app_context():
       return self.run(*args,**kwargs)
       

cel.Task = AppContextTask