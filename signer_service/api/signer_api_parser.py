from flask_restx import reqparse
from werkzeug.datastructures import FileStorage


class SignerApiParser:
    def __init__(self):
        pass

    @staticmethod
    def get_parser_post_signer():
        parser = reqparse.RequestParser()
        parser.add_argument("apk", type=FileStorage, location="files", help="APK file")
        return parser

    @staticmethod
    def get_parser_get_signer():
        parser = reqparse.RequestParser()
        parser.add_argument("job_id", type=str, help="Job ID to download")
        return parser
