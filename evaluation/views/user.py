from evaluation.views.utils import *


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
            if not User.check_exist(email):
                User.create(password, email, name, phone, avatar)
                return HttpResponse("Signup successfully")
            else:
                return HttpResponse("Account exist")
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_401_UNAUTHORIZED, content_type="text")

    @staticmethod
    @api_view(['GET'])
    def get_all(request):
        data = list(User.objects.values())
        return JsonResponse(data, safe=False)

    @staticmethod
    @api_view(['GET'])
    def get(request):
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"]
                user = User.get(token.split()[1])
                return Response(model_to_dict(user))
            except Exception as e:
                return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")
        return HttpResponse("token invalid", status=status.HTTP_401_UNAUTHORIZED, content_type="text")

    @staticmethod
    @api_view(['POST'])
    def signin(request):
        try:
            body = load_request_body(request)
            password = body["password"]
            email = body["email"]
            result = User.login(email, password)
            if result == "":
                return HttpResponse("Username or password is incorrect",
                                    status=status.HTTP_401_UNAUTHORIZED, content_type='text')
            return HttpResponse(result, content_type='text')
        except Exception as e:
            return HttpResponse(e.__str__(), status=status.HTTP_501_NOT_IMPLEMENTED, content_type="text")
