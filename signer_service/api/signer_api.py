import os
import uuid

from flask import send_file
from flask_restx import Namespace, Resource, abort
from werkzeug.datastructures import FileStorage

from signer_service.api.signer_api_parser import SignerApiParser
from signer_service.celery import CelerySignerManager
from signer_service.celery.tasks.signer.apk_signer_task import ApkSignerTask
from signer_service.commons.file_utils import FileUtils
from signer_service.commons.operation_result import OperationStatus
from signer_service.signing.signing_service import SigningService

signer_api = Namespace("signer", description="APK Signer operations")


class SignerEndpoint(Resource):
    def __init__(
        self,
        self_api,
        apk_signer_task: ApkSignerTask,
        signing_service: SigningService,
        celery_signer_manager: CelerySignerManager,
        tmp_dir: str,
        *args,
        **kwargs,
    ):
        super().__init__(self_api, *args, **kwargs)
        self.__apk_signer_task = apk_signer_task
        self.__signing_service = signing_service
        self.__celery_signer_manager = celery_signer_manager
        self.__tmp_dir = tmp_dir

    @signer_api.expect(SignerApiParser.get_parser_post_signer())
    @signer_api.response(201, "Job was created, started signing process")
    @signer_api.response(400, "Invalid APK")
    @signer_api.response(401, "Unauthorized. JWT validation failed")
    @signer_api.response(415, "Unsupported media type")
    @signer_api.response(500, "An unknown system error occurred, please try again")
    @signer_api.response(503, "The system is down for maintenance, please try again")
    def post(self):
        parser = SignerApiParser.get_parser_post_signer()
        args = parser.parse_args()

        apk_path = os.path.join(self.__tmp_dir, uuid.uuid4().hex + ".apk")

        # if you need to know APK packageName beforehand, you can get it through
        #   args.package_name
        self.__upload(args.apk, apk_path)

        task = self.__apk_signer_task.delay(apk_path)
        return {"job_id": task.id, "status": "STARTED"}, 201

    def __upload(self, apk_file: FileStorage, apk_path: str):
        os.makedirs(self.__tmp_dir, exist_ok=True)
        if apk_file.mimetype == "application/vnd.android.package-archive":
            apk_file.save(apk_path)
        else:
            abort(
                code=415,
                error="ERROR-415-1",
                status=None,
                message=f"Unsupported media type '{apk_file.mimetype}'. APK file expected",
            )

    @signer_api.expect(SignerApiParser.get_parser_get_signer())
    @signer_api.response(200, "Success")
    @signer_api.response(401, "Unauthorized. JWT validation failed")
    @signer_api.response(404, "Job not found")
    @signer_api.response(500, "An unknown system error occurred, please try again")
    @signer_api.response(503, "The system is down for maintenance, please try again")
    def get(self):
        parser = SignerApiParser.get_parser_get_signer()
        args = parser.parse_args()

        status = self.__celery_signer_manager.get_job_status(args.job_id)
        if status in ["PENDING", "FAILURE"]:
            abort(
                code=404,
                error="ERROR-404-2",
                status=None,
                message=f"Unable to find job_id '{args.job_id}'",
            )
        elif status in ["STARTED", "RETRY"]:
            return {"job_id": args.job_id, "status": "PROCESSING"}, 202
        elif status == "SUCCESS":
            operation_result = self.__celery_signer_manager.get_job_result(args.job_id)
            if operation_result.status == OperationStatus.NOT_FOUND:
                abort(
                    code=404,
                    error="ERROR-404-1",
                    status=None,
                    message=f"Couldn't find APK files for job_id '{args.job_id}'",
                )
            elif operation_result.status == OperationStatus.SUCCESS:
                apk_path = operation_result.data
                filename = FileUtils.get_filename_from_path(apk_path)
                if not os.path.isfile(apk_path):
                    abort(
                        code=404,
                        error="ERROR-404-1",
                        status=None,
                        message=f"Couldn't find APK files for job_id '{args.job_id}'",
                    )
                return send_file(
                    apk_path, attachment_filename=filename, as_attachment=True
                )
        else:
            abort(
                code=500,
                error="ERROR-500-1",
                status=None,
                message="An unexpected error has occurred",
            )
