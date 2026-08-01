import os
from flask import Flask, render_template
from flask_migrate import Migrate

from models import db
from routers.routes import shipment_bp
from controllers.utils import error_response


def create_app():
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('config.production.ProductionConfig')
    else:
        app.config.from_object('config.dev_config.DevConfig')

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(shipment_bp)

    @app.errorhandler(404)
    def not_found(e):
        return error_response('Endpoint not found', 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error_response('Method not allowed', 405)

    @app.errorhandler(500)
    def internal_error(e):
        return error_response('Internal server error', 500)

    @app.route('/')
    def health_check():
        return {'status': 'ok', 'service': 'Shipment Order API'}, 200

    @app.route('/dashboard')
    def dashboard():
        return render_template('index.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))