from flask import Flask, request
from flask_restx import abort
from werkzeug.middleware.proxy_fix import ProxyFix

from signer_service.flask.authentication.authentication_manager import AuthenticationManager


class FlaskWrapper:
    def __init__(self, app_name: str, authentication_manager: AuthenticationManager):
        self.__app = Flask(app_name.lower())
        self.__config_app(self.__app)

        @self.__app.before_request
        def before_request_func():
            if not authentication_manager.validate(request):
                abort(
                    code=401,
                    error="ERROR-401",
                    status="UNAUTHORIZED",
                    message="Invalid Authorization",
                )

    def __config_app(self, flask_app: Flask):
        flask_app.config["ERROR_404_HELP"] = False
        flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_for=1)

    def get_app(self) -> Flask:
        return self.__app
