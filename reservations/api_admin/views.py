import json
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import HttpRequest


def admin_login(request: HttpRequest):
    """
    リクエストとユーザー方法を照合する
    合致したばあい、
    """
    if request.method == "POST":
        # リクエストからユーザー名とパスワードを取得
        print(request.content_params)
        print(request.content_type)
        data: dict = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")

        # ユーザー認証
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            print("tokenKey=", token.key)
            return JsonResponse(
                {
                    "message": "ログインに成功しました",
                    "user": {"username": user.username},
                    "token": token.key,
                }
            )
        else:
            # ログイン失敗
            return JsonResponse(
                {"error": "ユーザー名またはパスワードが正しくありません"}, status=400
            )
    else:
        return JsonResponse(
            {"error": "POSTメソッドでリクエストしてください"}, status=405
        )
