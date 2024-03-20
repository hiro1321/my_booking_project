
# # ベースイメージを指定
# FROM python:3.9

# # 作業ディレクトリを設定
# WORKDIR /my_booking_project

# # Pythonの依存関係をインストール
# COPY requirements.txt /my_booking_project/
# RUN pip install --no-cache-dir -r requirements.txt

# # アプリケーションのソースコードをコピー
# COPY . .

# # ポートを公開
# EXPOSE 8000

# # アプリケーションの起動コマンド
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
