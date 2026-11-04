from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("juegos/", include("catalog.urls")),
    path("cursos/", include("courses.urls")),
    path("mi-panel/", include("enrollments.urls")),
    path("", include("core.urls")),
]
