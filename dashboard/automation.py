import time
from .models import Task, TaskLog

def run_email_task(task_id):
    """
    Simulates sending an email.
    """
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'running'
        task.save()

        # Simulate work
        time.sleep(2)

        # Log success
        TaskLog.objects.create(
            task=task,
            status='completed',
            status_message='Email sent successfully.'
        )

        task.status = 'completed'
        task.save()
        return True
    except Exception as e:
        if 'task' in locals():
            task.status = 'failed'
            task.save()
            TaskLog.objects.create(
                task=task,
                status='failed',
                status_message=str(e)
            )
        return False

def run_scraping_task(task_id):
    """
    Simulates a web scraping task.
    """
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'running'
        task.save()

        # Simulate work
        time.sleep(3)

        # Log success
        TaskLog.objects.create(
            task=task,
            status='completed',
            status_message='Scraped data from 5 pages.'
        )

        task.status = 'completed'
        task.save()
        return True
    except Exception as e:
        if 'task' in locals():
            task.status = 'failed'
            task.save()
            TaskLog.objects.create(
                task=task,
                status='failed',
                status_message=str(e)
            )
        return False
