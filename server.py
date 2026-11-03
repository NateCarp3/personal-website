from flask_app import app
from flask_app.controllers import nates  # noqa: F401  (registers the routes)
from flask_app.models import nate  # noqa: F401

if __name__ == "__main__":
    app.run(debug=True)
