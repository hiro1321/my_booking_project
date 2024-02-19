import json
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


@api_view(["POST"])
def admin_login(request: HttpRequest):
    """
    リクエストとユーザー情報を照合する
    照合できた場合、認証トークンを返す
    """
    # リクエストからユーザー名とパスワードを取得
    username = request.data.get("username")
    password = request.data.get("password")

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


@api_view(["POST"])
def verify_token(request):
    """
    リクエストのトークンを取得しログイン中か否かを判定
    """
    token_key: str = request.data.get("token")
    # トークンが存在するかチェック
    if not token_key:
        return Response(
            {"error": "トークンが提供されていません"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return Response(
            {"error": "トークンが無効です"}, status=status.HTTP_401_UNAUTHORIZED
        )

    return Response({"message": "トークンが検証されました"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def admin_logout(request: HttpRequest):
    """ユーザーをログアウト状態にし、認証トークンも削除"""
    logout(request)
    token = Token.objects.get(key=request.data.get("token"))
    token.delete()
    return Response({"message": "ログアウトしました"}, status=status.HTTP_200_OK)
