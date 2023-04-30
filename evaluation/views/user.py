from .utils import *


class UserView:
    @staticmethod
    @api_view(['POST'])
    def signup(request, format=None):
        try:
            body = load_request_body(request)
            for i in ["email", "password", "name"]:
                if i not in body:
                    raise Exception('Email, password and name are required')
            email = body["email"]
            password = body["password"]
            name = body["name"]
            phone = body["phone"] if "phone" in body else ""
            avatar = body["avatar"] if "avatar" in body else ""
            return HttpResponse(UserUsecase.signup(password, email, name, phone, avatar))
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def verify(request, token):
        try:
            email = get_email_from_token(token)
            UserUsecase.verify(email)
            return HttpResponse('Verify successfully<br>Please <a href="http://localhost:5173/login">login</a> to use BPSky')
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")

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
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")
