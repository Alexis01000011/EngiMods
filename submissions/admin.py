from django.contrib import admin

from .models import Submission, SubmissionAttempt


class SubmissionAttemptInline(admin.StackedInline):
    model = SubmissionAttempt
    fields = ("repository_url", "comment", "game_version", "modding_environment", "submitted_at")
    extra = 0


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "exercise", "status", "created_at")
    list_filter = ("status", "enrollment__course")
    search_fields = ("enrollment__user__email", "exercise__title")
    list_select_related = ("enrollment__user", "enrollment__course", "exercise")
    raw_id_fields = ("enrollment",)
    inlines = (SubmissionAttemptInline,)
