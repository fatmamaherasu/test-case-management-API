import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
from routes import test_cases
from dotenv import load_dotenv, dotenv_values


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(test_cases)
    #app.config.from_mapping(dotenv_values())
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.engine = create_engine("sqlite:///./tests.db", echo=True)
    Session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=app.engine))
    app.session = Session

    Base.query = app.session.query_property()
    Base.metadata.drop_all(bind=app.engine)
    Base.metadata.create_all(bind=app.engine)

    return app
