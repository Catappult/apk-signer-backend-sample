from signer_service.flask.authentication.authentication_provider import (
    authentication_provider,
)
from signer_service.flask.flask_wrapper import FlaskWrapper


class FlaskProvider:
    def __init__(self):
        self.__authentication_manager = (
            authentication_provider.provide_authentication_manager()
        )

    def provide_flask_wrapper(self, app_name: str) -> FlaskWrapper:
        return FlaskWrapper(app_name, self.__authentication_manager)


flask_provider = FlaskProvider()
