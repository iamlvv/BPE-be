from evaluation.views.utils import *


class EvaluateView:
    @staticmethod
    @api_view(['POST'])
    def evaluate(request, format=None):
        body = load_request_body(request)
        result = Evaluate.evaluate(body)
        json_response = [r.__dict__ for r in result]
        return JsonResponse(json_response, safe=False)
