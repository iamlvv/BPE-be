from evaluation.views.utils import *


class EvaluatedResultView:
    @staticmethod
    @api_view(['POST'])
    def get_result_by_bpmn_file(request):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            data = EvaluatedResultUsercase.get_all_result_by_bpmn_file(
                user_id, body['projectID'], body['xmlFileLink'])
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def save(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            xml_file_link = body['xmlFileLink']
            # project_id = body['projectID']
            name = body['name']
            result = body['result']
            description = body['description']
            project_start_time = body['projectStartTime']
            base_time_unit = body['baseTimeUnit']
            base_currency_unit = body['baseCurrencyUnit']
            EvaluatedResultUsercase.save(user_id, xml_file_link, project_id, name, result,
                                         description, project_start_time, base_time_unit, base_currency_unit)
            return HttpResponse("Create successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def get(request):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            data = EvaluatedResultUsercase.get_result(
                user_id, body['projectID'],  body['xmlFileLink'], body['name'])
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['DELETE'])
    def delete(request):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            EvaluatedResultUsercase.delete(
                user_id,  body['xmlFileLink'], body['projectID'], body['name'])
            return HttpResponse("Delete successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")
