from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("evaluation.urls.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
