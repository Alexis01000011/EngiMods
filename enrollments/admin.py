from django.contrib import admin

from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "origin", "status", "enrolled_at", "access_ends_at")
    list_filter = ("origin", "status", "course")
    search_fields = ("user__email", "user__display_name", "course__title")
    list_select_related = ("user", "course")
    raw_id_fields = ("user",)
