from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("juegos/", include("catalog.urls")),
    path("cursos/", include("payments.urls")),
    path("cursos/", include("courses.urls")),
    path("mi-panel/", include("enrollments.urls")),
    path("mi-panel/entregas/", include("submissions.urls")),
    path("tutoria/entregas/", include("submissions.tutor_urls")),
    path("", include("core.urls")),
]
