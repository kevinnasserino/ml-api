from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    @app.route("/")
    def health_check():
        return {"message": "API is running!"}

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 8080))  # Default ke 8080 jika PORT tidak diatur
    app.run(host="0.0.0.0", port=port)
