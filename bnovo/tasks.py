from celery import Celery
import requests
from .views import get_all_booking, session

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def check():
    print('Reprint every 10 seconds')
    s = get_all_booking(session)
    print(s)

app.conf.beat_schedule = {
    'run-me-every-ten-seconds': {
        'task': 'tasks.check',
        'schedule': 10.0
    }
}

if __name__ == '__main__':
    check()
