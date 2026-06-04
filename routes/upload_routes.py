from flask import Blueprint
from services.csv_upload_service import CsvUploadService

upload_bp = Blueprint("upload", __name__)

csv_service = CsvUploadService()


@upload_bp.route("/upload", methods=["Post"])
def upload_csv():
    return csv_service.upload_csv(None)
    
