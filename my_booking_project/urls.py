from django.contrib import admin
from django.urls import include, path
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from reservations.top import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("api/", include("reservations.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
