from evaluation.views.utils import *


class BPMNFileView:
    @staticmethod
    @api_view(['PUT'])
    def save(request, project_id, version):
        try:
            user_id = get_id_from_token(get_token(request))
            if "file" not in request.FILES:
                raise Exception("file required")
            if "xmlFileLink" not in request.POST:
                raise Exception("xmlFileLink required")
            file = request.FILES['file']
            xml_file_link = request.POST['xmlFileLink']
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
            if "file" not in request.FILES:
                raise Exception("file required")
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

    @staticmethod
    @api_view(['GET'])
    def get_content_by_version(request, project_id, version):
        try:
            user_id = get_id_from_token(get_token(request))
            versions = BPMNFileUsecase.get_content_by_version(
                user_id, project_id, version)
            return HttpResponse(versions, content_type="xml")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def comment(request):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            for i in ["projectID", "xmlFileLink", "content"]:
                if i not in body:
                    raise Exception(i + " required")
            project_id = body['projectID']
            xml_file_link = body['xmlFileLink']
            content = body['content']
            BPMNFileUsecase.comment(
                user_id, project_id, xml_file_link, content)
            return HttpResponse("Comment successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['PUT'])
    def edit_comment(request):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            for i in ["projectID", "xmlFileLink", "id", "content"]:
                if i not in body:
                    raise Exception(i + " required")
            project_id = body['projectID']
            xml_file_link = body['xmlFileLink']
            id = body['id']
            content = body['content']
            BPMNFileUsecase.edit_comment(
                user_id, project_id, xml_file_link, id, content)
            return HttpResponse("Edit successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['DELETE'])
    def delete_comment(request):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            for i in ["projectID", "xmlFileLink", "id"]:
                if i not in body:
                    raise Exception(i + " required")
            project_id = body['projectID']
            xml_file_link = body['xmlFileLink']
            id = body['id']
            BPMNFileUsecase.delete_comment(
                user_id, project_id, xml_file_link, id)
            return HttpResponse("Delete successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def get_comment_by_bpmn_file(request):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            for i in ["projectID", "xmlFileLink"]:
                if i not in body:
                    raise Exception(i + " required")
            project_id = body['projectID']
            xml_file_link = body['xmlFileLink']
            data = BPMNFileUsecase.get_comment_by_bpmn_file(
                user_id, project_id, xml_file_link)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def get_comment_by_user(request):
        try:
            user_id = get_id_from_token(get_token(request))
            data = BPMNFileUsecase.get_comment_by_user(user_id)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def get_image_by_bpmn_file(request):
        try:
            user_id = get_id_from_token(get_token(request))
            body = load_request_body(request)
            for i in ["projectID", "xmlFileLink"]:
                if i not in body:
                    raise Exception(i + " required")
            project_id = body['projectID']
            xml_file_link = body['xmlFileLink']
            data = ImageUsecase.get_image_by_bpmn_file(
                user_id, project_id, xml_file_link)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def add_image(request):
        try:
            user_id = get_id_from_token(get_token(request))
            if "file" not in request.FILES:
                raise Exception("file required")
            for i in ["projectID", "xmlFileLink"]:
                if i not in request.POST:
                    raise Exception(i + " required")
            file = request.FILES['file']
            project_id = request.POST['projectID']
            xml_file_link = request.POST['xmlFileLink']
            ImageUsecase.insert_image(
                user_id, project_id, xml_file_link, file)
            return HttpResponse("Create successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="text")
