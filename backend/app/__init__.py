from flask import Flask, jsonify
from .config import Config
from .extensions import db, jwt, bcrypt, cors


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Bind extensions to the app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # Import models so create_all() sees them
    from . import models  # noqa

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app