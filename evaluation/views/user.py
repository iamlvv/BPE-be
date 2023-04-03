from evaluation.views.utils import *


class UserView:
    @staticmethod
    @api_view(['POST'])
    def insert(request, format=None):
        body = load_request_body(request)
        password = body["password"]
        name = body["name"]
        email = body["email"]
        phone = body["phone"]
        avatar = body["avatar"]
        user = User.create(password, email, name, phone, avatar)
        user.save()
        return Response("Insert successfully")

    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        data = list(User.objects.values())
        return JsonResponse(data, safe=False)
