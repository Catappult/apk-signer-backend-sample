from flask_restx import Api

from signer_service.api.default_api import StatusEndpoint


class DefaultApiFactory:
    def __init__(self):
        pass

    def create_namespace(self, api: Api):
        api.add_resource(
            StatusEndpoint,
            "/status",
            methods=["GET"],
            resource_class_kwargs={},
        )
