from flask import Flask
from config import Config

from models import db

from routes.auth import auth
from routes.project import project
from routes.bug import bug


app = Flask(__name__)


app.secret_key = "bugtracking123"

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(project)
app.register_blueprint(bug)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)