from config_loader import configs


class CelerySignerConfig:
    name = "signer"
    enable_utc = True
    timezone = "Europe/London"
    broker_url = configs["celery"]["redis"]["broker_url"]
    result_backend = configs["celery"]["redis"]["result_backend"]
    accept_content = ["json", "pickle"]
    result_serializer = "pickle"
    task_track_started = True
