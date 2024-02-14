import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import HttpRequest


def admin_login(request: HttpRequest):
    if request.method == "POST":
        # リクエストからユーザー名とパスワードを取得
        print(request.content_params)
        print(request.content_type)
        data: dict = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")

        print(username)
        print(password)

        # ユーザー認証
        user = authenticate(username=username, password=password)

        if user is not None:
            # ログイン成功
            login(request, user)
            return JsonResponse(
                {
                    "message": "ログインに成功しました",
                    "user": {"username": user.username},
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
