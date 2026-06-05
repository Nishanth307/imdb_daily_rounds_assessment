from flask import jsonify 
from utils.exceptions import AppException

def register_error_handlers(app):

    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return jsonify({
            "success": False,
            "message": error.message,
        }), error.status_code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
            "success":False,
            "message":"Something went wrong"
        }), 500

    
        