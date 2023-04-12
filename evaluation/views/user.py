from .utils import *


class UserView:
    @staticmethod
    @api_view(['POST'])
    def signup(request, format=None):
        try:
            body = load_request_body(request)
            password = body["password"]
            name = body["name"]
            email = body["email"]
            phone = body["phone"]
            avatar = body["avatar"]
            return HttpResponse(UserUsecase.signup(password, email, name, phone, avatar))
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_401_UNAUTHORIZED, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        data = UserUsecase.get_all()
        return JsonResponse(data, safe=False)

    @staticmethod
    @api_view(['GET'])
    def get(request):
        try:
            user = UserUsecase.get(get_token(request))
            return Response(user)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def signin(request):
        try:
            body = load_request_body(request)
            password = body["password"]
            email = body["email"]
            result = UserUsecase.signin(email, password)
            return HttpResponse(result, content_type='text')
        except Exception as e:
            return HttpResponse("Username or password is incorrect", status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")
