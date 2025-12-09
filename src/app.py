from flask import Flask
# from app.config import settings
from api.controllers import generator_controller, reviewer_controller, nlp_tests_controller
import json


app = Flask(__name__)
app.register_blueprint(generator_controller, url_prefix="/llm-generator")
app.register_blueprint(reviewer_controller, url_prefix="/llm-reviewer")
app.register_blueprint(nlp_tests_controller, url_prefix="/nlp-tests")

@app.route("/")
def home():
    return "App is running."



if __name__ == "__main__":
    app.run(debug=True)