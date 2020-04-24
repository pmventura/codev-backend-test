from flask import Flask
from flask_restplus import Api


def create_app():
    """
    Initialize the core application.
    :return app:
    """

    app = Flask(__name__)
    app.config.from_object('config.Config')
    api = Api(app)

    with app.app_context():

        from app.resources.users import User

        api.add_resource(User, "/api/v1/users")

    return app

