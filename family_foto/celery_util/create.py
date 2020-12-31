def init_celery(celery, app):
    """
    Initializes a celery worker.
    :param celery: Celery Instance
    :param app: the app calling the celery worker
    """
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
