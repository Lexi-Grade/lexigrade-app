from flask import Blueprint
from flask_pydantic import validate
from api.interfaces import LLMReviewerInterface
from config import settings
from http import HTTPStatus
import requests

nlp_tests_controller = Blueprint('nlp_tests_controller', __name__)

@nlp_tests_controller.route("/execute", methods=["POST"])
@validate()
def execute_tests(body: LLMReviewerInterface):
    print()
