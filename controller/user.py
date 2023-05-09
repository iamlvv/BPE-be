from .utils import *
from oauth2.google import LoginWithGoogle


@bpsky.route("/user/signup", methods=["POST"])
def user_signup():
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
        return UserUsecase.signup(password, email, name, phone, avatar)
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/user/verify/<string:token>", methods=["GET"])
def user_verify(token):
    host = os.environ.get("HOST")
    try:
        email = get_email_from_token(token)
        UserUsecase.verify(email)
        return redirect(f"{host}/login")
    except Exception as e:
        return redirect(f"{host}/login")


@bpsky.route("/user/resend", methods=["POST"])
def user_resend_email():
    try:
        body = load_request_body(request)
        if "email" not in body:
            raise Exception('email required')
        email = body['email']
        UserUsecase.resend_email(email)
        return "Resend successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/user/all", methods=["GET"])
def user_get_all():
    data = UserUsecase.get_all()
    return bpsky.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


@bpsky.route("/user", methods=["GET"])
def user_get():
    try:
        user = UserUsecase.get(get_token(request))
        return bpsky.response_class(
            response=json.dumps(user),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/user/signin", methods=["POST"])
def user_signin():
    try:
        body = load_request_body(request)
        for i in ["email", "password"]:
            if i not in body:
                raise Exception(i + " required")
        password = body["password"]
        email = body["email"]
        msg = UserUsecase.signin(email, password)
        return msg
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/user/reset", methods=["POST"])
def user_reset_password():
    try:
        body = load_request_body(request)
        if "email" not in body:
            raise Exception('email required')
        email = body['email']
        UserUsecase.reset_password(email)
        return "Send email successfully"
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/user/search", methods=["GET"])
def user_search():
    try:
        get_email_from_token(get_token(request))
        s = request.args.get('s', '')
        if s == '':
            raise Exception('bad request')
        data = UserUsecase.search(s)
        return bpsky.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/auth/login/google", methods=["GET"])
def user_auth_with_google():
    try:
        request_uri = LoginWithGoogle.login()
        return redirect(request_uri)
    except Exception as e:
        return bpsky.response_class(
            response=e.__str__(),
            status=500
        )


@bpsky.route("/auth/login/google/callback", methods=["GET"])
def user_callback():
    host = os.environ.get("HOST")
    try:
        code = request.args.get("code")
        data = LoginWithGoogle.get(request.url, code)
        token = UserUsecase.auth_with_google(data[1], data[2], data[3])
        return redirect(f"{host}?token={token}")
    except Exception as e:
        return redirect(f"{host}/login")