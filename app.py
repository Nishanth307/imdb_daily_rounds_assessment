from flask import Flask
from routes.upload_routes import upload_bp
from routes.movie_routes import movie_bp
from utils.error_handler import register_error_handlers

app = Flask(__name__)

app.register_blueprint(upload_bp, url_prefix="/api/v1")
app.register_blueprint(movie_bp, url_prefix="/api/v1")
register_error_handlers(app)


@app.route("/", methods=["GET"])
def health():
    return {"status": "running", "service": "imdb-content-system"}


@app.errorhandler(Exception)
def handle_exception(error):
    return {"success": False, "message": str(error)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
