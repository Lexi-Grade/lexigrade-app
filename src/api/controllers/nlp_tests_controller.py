from flask import Blueprint
from flask_pydantic import validate
from api.interfaces import NLPTests
from services.nlp_tests import LexicalComplexityTests
from config import settings
from http import HTTPStatus
import requests

nlp_tests_controller = Blueprint('nlp_tests_controller', __name__)

@nlp_tests_controller.route("/hard-constraints/execute", methods=["POST"])
@validate()
def execute_hard_constraints_tests(body: NLPTests):
    complexity_tester = LexicalComplexityTests(language=body.language, target_level=body.cefr_level_target)
    cefr_validity_result = complexity_tester.check_cefr_validity(body.simplified_text)
    oov_result = complexity_tester.check_oov(body.simplified_text)
    difficult_word_ration = complexity_tester.check_difficult_word_ratio(body.simplified_text)
    if (cefr_validity_result['status'] == 'fail' or
        oov_result['status'] == 'fail' or
        difficult_word_ration['status'] == 'fail'):
        http_status = HTTPStatus.BAD_REQUEST
    else:
        http_status = HTTPStatus.OK
    return {
        "cefr_validity": cefr_validity_result,
        "oov": oov_result,
        "difficult_word_ratio": difficult_word_ration
    }, http_status
