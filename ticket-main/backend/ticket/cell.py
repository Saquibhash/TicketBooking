from ticket.worker import cel
from ticket import tasks
from flask import Flask, request
from celery.result import AsyncResult
from celery.schedules import crontab
from ticket import create_app 
from .worker import create_celery_app

app = create_app()
# cel_app = cel
cel_app = create_celery_app(app)

@cel_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    
     
    # # #daily reminder test 
    # sender.add_periodic_task(10.0, tasks.send_daily.s())
    # # #monthly report test 
    # sender.add_periodic_task(30.0, tasks.send_mr.s())
     
    
    #scheduled task for daily reminder at 7pm
    sender.add_periodic_task(
        crontab(minute=0, hour=19),
        tasks.send_daily.s(),
        name='Daily reminder everyday @7PM via mail.')
     
    #scheduled report sending on every 1st of month
    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        tasks.send_mr.s(),
        name='Monthly Entertainment report on 1st of every month.')
   
if __name__ == '__main__':
    cel_app.start()
# if __name__ == '__main__':
#     cel_app.run(debug=True)
