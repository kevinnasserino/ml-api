from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import blueprints
    from .cbf import cbf_blueprint
    from .tsp import tsp_blueprint

    # Register blueprints
    app.register_blueprint(cbf_blueprint, url_prefix='/cbf')
    app.register_blueprint(tsp_blueprint, url_prefix='/tsp')

    return app
