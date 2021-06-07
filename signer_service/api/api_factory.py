from flask import url_for
from flask_restx import Api

from .default_api_factory import DefaultApiFactory
from .signer_api_factory import SignerApiFactory


class SwaggerApi(Api):
    """
    This is a modification of the base Flask Restplus Api class due
    to the issue described here
    https://github.com/noirbizarre/flask-restplus/issues/223
    """

    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`)
        :rtype: str
        """
        return url_for(self.endpoint("specs"), _external=False)


class ApiFactory:
    def __init__(
        self,
        default_api_factory: DefaultApiFactory,
        signer_api_factory: SignerApiFactory,
    ):
        self.__api = None
        self.__default_api_factory = default_api_factory
        self.__signer_api_factory = signer_api_factory

    def get_api(self):
        if not self.__api:
            self.__api = self.__create_api()
        return self.__api

    def __create_api(self) -> SwaggerApi:
        api = SwaggerApi(
            version="0.1",
            title="Signer API",
            description="APK Signer Backend Sample",
        )
        self.__default_api_factory.create_namespace(api)
        self.__signer_api_factory.create_namespace(api)

        @api.errorhandler
        def default_error_handler(error):
            return {"message": "Internal Server Error"}, getattr(error, "code", 500)

        return api
