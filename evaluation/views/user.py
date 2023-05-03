from .utils import *
from evaluation.oauth2.google import LoginWithGoogle


class UserView:
    @staticmethod
    @api_view(['POST'])
    def signup(request, format=None):
        try:
            body = load_request_body(request)
            for i in ["email", "password", "name"]:
                if i not in body:
                    raise Exception(i + " required")
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
        host = os.environ.get("HOST")
        try:
            email = get_email_from_token(token)
            UserUsecase.verify(email)
            return HttpResponseRedirect(f"{host}/login")
        except Exception as e:
            return HttpResponseRedirect(f"{host}/login")

    @staticmethod
    @api_view(['POST'])
    def resend_email(request):
        try:
            body = load_request_body(request)
            if "email" not in body:
                raise Exception('email required')
            email = body['email']
            UserUsecase.resend_email(email)
            return HttpResponse("Resend successfully")
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
            for i in ["email", "password"]:
                if i not in body:
                    raise Exception(i + " required")
            password = body["password"]
            email = body["email"]
            result = UserUsecase.signin(email, password)
            return HttpResponse(result, content_type='text')
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def reset_password(request):
        try:
            body = load_request_body(request)
            if "email" not in body:
                raise Exception('email required')
            email = body['email']
            UserUsecase.reset_password(email)
            return HttpResponse("Send email successfully")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def search(request):
        try:
            get_email_from_token(get_token(request))
            s = request.GET.get('s', '')
            if s == '':
                raise Exception('bad request')
            data = UserUsecase.search(s)
            return JsonResponse(data, safe=False)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def auth_with_google(request):
        try:
            request_uri = LoginWithGoogle.login()
            return HttpResponseRedirect(request_uri)
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def callback(request):
        host = os.environ.get("HOST")
        try:
            code = request.GET.get("code")
            data = LoginWithGoogle.get(request, code)
            token = UserUsecase.auth_with_google(data[1], data[2], data[3])
            return HttpResponseRedirect(f"{host}?token={token}")
        except Exception as e:
            return HttpResponseRedirect(f"{host}/login")
