from evaluation.views.utils import *


class BPMNFileView:
    @staticmethod
    @api_view(['PUT'])
    def save(request, project_id, version):
        try:
            user_id = get_id_from_token(get_token(request))
            file = request.FILES['file']
            xml_file_link = request.POST['xml_file_link']
            BPMNFileUsecase.save(xml_file_link, file,
                                 user_id, project_id, version)
            return HttpResponse("Save successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def create_new_version(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            file = request.FILES['file']
            BPMNFileUsecase.create_new_version(user_id, file, project_id)
            return HttpResponse("Create successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['DELETE'])
    def delete_oldest_version(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            BPMNFileUsecase.delete_oldest_version(user_id, project_id)
            return HttpResponse("Delete successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['DELETE'])
    def delete_version(request, project_id, version):
        try:
            user_id = get_id_from_token(get_token(request))
            BPMNFileUsecase.delete_version(user_id, project_id, version)
            return HttpResponse("Delete successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def get_by_project(request, project_id):
        try:
            user_id = get_id_from_token(get_token(request))
            versions = BPMNFileUsecase.get_by_project(user_id, project_id)
            return JsonResponse(versions, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def get_by_version(request, project_id, version):
        try:
            user_id = get_id_from_token(get_token(request))
            versions = BPMNFileUsecase.get_by_version(
                user_id, project_id, version)
            return JsonResponse(versions, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")
