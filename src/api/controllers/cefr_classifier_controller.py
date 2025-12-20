from flask import Blueprint
from flask_pydantic import validate
from api.interfaces import CEFRClassifier
from api.services import SupervisedCEFREstimationService, NLPBasedCEFRClassifier
from http import HTTPStatus

cefr_classifier_controller = Blueprint('cefr_classifier_controller', __name__)

@cefr_classifier_controller.route("/estimate", methods=["POST"])
@validate()
def estimate_cefr(body: CEFRClassifier):
    if body.language == "english":
        cefr_classifier = SupervisedCEFREstimationService(language=body.language)
    else:
        cefr_classifier = NLPBasedCEFRClassifier(language=body.language)

    result = cefr_classifier.estimate(body.text)
    return result, HTTPStatus.OK

