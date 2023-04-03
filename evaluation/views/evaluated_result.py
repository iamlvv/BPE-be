from evaluation.views.utils import *


class EvaluatedResultView:
    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        data = list(EvaluatedResult.objects.values())
        return JsonResponse(data, safe=False)

    @staticmethod
    @api_view(['POST'])
    def save(request):
        body = load_request_body(request)
        EvaluatedResult.insert(
            body["xmlFileLink"],
            body['projectID'],
            body['result'],
        )
        return Response("Save successfully")
