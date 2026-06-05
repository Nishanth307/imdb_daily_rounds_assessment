from flask import Blueprint, request
from services.csv_upload_service import CsvUploadService

upload_bp = Blueprint("upload", __name__)

csv_service = CsvUploadService()


@upload_bp.route("/upload", methods=["Post"])
def upload_csv():
    file = request.files.get("file")
    return csv_service.upload_csv(file)
