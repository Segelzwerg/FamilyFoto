def init_celery(celery, app):
    """
    Initializes a celery_worker worker.
    :param celery: Celery Instance
    :param app: the app calling the celery_worker worker
    """
    celery.conf.update(app.config)

    # pylint: disable=too-few-methods
    class ContextTask(celery.Task):
        """
        A task that has the app context forced pushed.
        """

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return celery.TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
