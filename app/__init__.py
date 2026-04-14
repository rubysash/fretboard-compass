"""
Application Factory for ChordDumper.
Initialized the Flask application and registers blueprints/routes.
"""
import logging
from flask import Flask
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup Logging
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=app.config['LOG_FORMAT']
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Starting ChordDumper in {'DEBUG' if app.config['DEBUG'] else 'PRODUCTION'} mode")
    
    @app.after_request
    def add_header(response):
        """Disable browser caching during development."""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    
    # Custom Filters
    import base64
    @app.template_filter('b64encode')
    def b64encode_filter(s):
        if isinstance(s, str):
            s = s.encode('utf-8')
        return base64.b64encode(s).decode('utf-8')
    
    with app.app_context():
        from .routes import main_bp
        app.register_blueprint(main_bp)
        return app
