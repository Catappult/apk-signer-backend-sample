from celery import Celery
from flask import Flask


class CeleryWrapper:
    def __init__(self):
        pass

    def build(self, flask_app: Flask, config: object) -> Celery:
        celery = Celery(flask_app.import_name)
        celery.config_from_object(config)

        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with flask_app.app_context():
                    return self.run(*args, **kwargs)

        celery.Task = ContextTask
        return celery
