from flask import Flask
from routes.upload_routes import upload_bp
from routes.movie_routes import movie_bp

app = Flask(__name__)

app.register_blueprint(upload_bp, url_prefix="/api/v1")
app.register_blueprint(movie_bp, url_prefix="/api/v1")


@app.route("/", methods=["GET"])
def health():
    return {"status": "running", "service": "imdb-content-system"}


if __name__ == "__main__":
    app.run(debug=True)
