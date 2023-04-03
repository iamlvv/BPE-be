from evaluation.views.utils import *


class ProjectView:
    @staticmethod
    @api_view(['POST'])
    def insert(request):
        body = load_request_body(request)
        Project.insert(body["document"], body["name"], body["user_id"])
        return Response("Insert successfully")

    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        return Project.get_all()
