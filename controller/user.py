from .utils import *
from oauth2.google import LoginWithGoogle


@bpsky.route("/api/v1/user/signup", methods=["POST"])
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
        response = UserUsecase.signup(password, email, name, phone, avatar)
        if response == "Account exist":
            return bpsky.response_class(response=response, status=500)
        else:
            personalWorkspace = WorkspaceUseCase.createNewWorkspace(
                name,
                "Personal workspace",
                datetime.now(),
                response["id"],
                "",
                "",
                True,
                False,
            )
        return bpsky.response_class(
            response=response,
            content_type="text",
            status=200,
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/verify/<string:token>", methods=["GET"])
def user_verify(token):
    host = os.environ.get("HOST")
    try:
        email = get_email_from_token(token)
        print("email: ", email)
        data = UserUsecase.verify(email)
        print("data", data)
        return redirect(f"{host}/login")
    except Exception as e:
        return redirect(f"{host}/login")


@bpsky.route("/api/v1/user/resend", methods=["POST"])
def user_resend_email():
    try:
        body = load_request_body(request)
        if "email" not in body:
            raise Exception("email required")
        email = body["email"]
        UserUsecase.resend_email(email)
        return "Resend successfully"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/all", methods=["GET"])
def user_get_all():
    data = UserUsecase.get_all()
    return bpsky.response_class(
        response=json.dumps(data), status=200, mimetype="application/json"
    )


@bpsky.route("/api/v1/user", methods=["GET"])
def user_get():
    try:
        id = get_id_from_token(get_token(request))
        user = UserUsecase.get(id)
        return bpsky.response_class(
            response=json.dumps(user), status=200, mimetype="application/json"
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/signin", methods=["POST"])
def user_signin():
    try:
        body = load_request_body(request)
        for i in ["email", "password"]:
            if i not in body:
                raise Exception(i + " required")
        password = body["password"]
        email = body["email"]
        token = UserUsecase.signin(email, password)
        return bpsky.response_class(response=token, content_type="text", status=200)
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/password", methods=["PUT"])
def user_change_password():
    try:
        email = get_email_from_token(get_token(request))
        body = load_request_body(request)
        if "newPassword" not in body:
            raise Exception("new password required")
        new_password = body["newPassword"]
        UserUsecase.change_password(email, new_password)
        return "Change successfully"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/reset", methods=["POST"])
def user_reset_password():
    try:
        body = load_request_body(request)
        if "email" not in body:
            raise Exception("email required")
        email = body["email"]
        UserUsecase.reset_password(email)
        return "Send email successfully"
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/user/search", methods=["GET"])
def user_search():
    try:
        email = get_email_from_token(get_token(request))
        s = request.args.get("s", "")
        workspaceId = request.args.get("workspaceId", None)
        if s == "":
            raise Exception("bad request")
        data = UserUsecase.search(s, email, workspaceId)
        return bpsky.response_class(
            response=json.dumps(data), status=200, mimetype="application/json"
        )
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/auth/login/google", methods=["GET"])
def user_auth_with_google():
    try:
        request_uri = LoginWithGoogle.login()
        return redirect(request_uri)
    except Exception as e:
        return bpsky.response_class(response=e.__str__(), status=500)


@bpsky.route("/api/v1/auth/login/google/callback", methods=["GET"])
def user_callback():
    host = os.environ.get("HOST")
    try:
        code = request.args.get("code")
        data = LoginWithGoogle.get(request.url, code)
        token = UserUsecase.auth_with_google(data[1], data[2], data[3])
        return redirect(f"{host}?token={token}")
    except Exception as e:
        return redirect(f"{host}/login")
