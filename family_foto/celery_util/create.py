def init_celery(celery, app):
    """
    Initializes a celery worker.
    :param celery: Celery Instance
    :param app: the app calling the celery worker
    """
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """
        A task that has the app context forced pushed.
        """

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return celery.TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
