from evaluation.views.utils import *


class ProjectView:
    @staticmethod
    @api_view(['POST'])
    def insert(request):
        try:
            body = load_request_body(request)
            user_id = get_id_from_token(get_token(request))
            ProjectUsecase.create(body["document"], body["name"], user_id)
            return HttpResponse("Insert successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def get_project(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            result = ProjectUsecase.get(project_id, user_id)
            return JsonResponse(result, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def get_all_project_by_user_id(request):
        try:
            user_id = get_id_from_token(get_token(request))
            result = ProjectUsecase.get_all_project_by_user_id(user_id)
            return JsonResponse(result, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        return JsonResponse(ProjectUsecase.get_all(), status=status.HTTP_200_OK, safe=False)

    @staticmethod
    @api_view(['GET'])
    def get_document(request, project_id):
        try:
            return HttpResponse(ProjectUsecase.get_document(project_id), status=status.HTTP_200_OK, content_type="text")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['PUT'])
    def update_document(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            return HttpResponse(ProjectUsecase.update_document(user_id, project_id, body['document']), status=status.HTTP_200_OK, content_type="text")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def get_all_user(request, project_id):
        try:
            return JsonResponse(ProjectUsecase.get_all_user_by_project_id(project_id), status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['PUT'])
    def update_all_user(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            if "user_id" not in body or "role" not in body:
                return HttpResponse("bad request", status=status.HTTP_400_BAD_REQUEST, content_type="text")
            return HttpResponse(ProjectUsecase.update_permission(user_id, body["user_id"], project_id, body["role"]), status=status.HTTP_200_OK, content_type="text")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['DELETE'])
    def revoke_user(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            if type(body) is not list:
                return HttpResponse("bad request", status=status.HTTP_400_BAD_REQUEST, content_type="text")
            return HttpResponse(ProjectUsecase.revoke_permission(user_id, body, project_id), status=status.HTTP_200_OK, content_type="text")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def grant_user(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            if "user_id" not in body or "role" not in body:
                return HttpResponse("bad request", status=status.HTTP_400_BAD_REQUEST, content_type="text")
            return HttpResponse(ProjectUsecase.grant_permission(user_id, body["user_id"], project_id, body["role"]), status=status.HTTP_200_OK, content_type="text")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")
