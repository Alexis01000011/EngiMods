from django.contrib import admin

from .models import Enrollment, LessonProgress


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "origin", "status", "enrolled_at", "access_ends_at")
    list_filter = ("origin", "status", "course")
    search_fields = ("user__email", "user__display_name", "course__title")
    list_select_related = ("user", "course")
    raw_id_fields = ("user",)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "lesson", "completed_at")
    list_filter = ("enrollment__course",)
    search_fields = ("enrollment__user__email", "lesson__title")
    list_select_related = ("enrollment__user", "enrollment__course", "lesson")
    raw_id_fields = ("enrollment", "lesson")
