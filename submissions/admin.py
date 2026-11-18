from django.contrib import admin

from .models import PublicationChecklist, Review, ReviewScore, Submission, SubmissionAttempt


class SubmissionAttemptInline(admin.StackedInline):
    model = SubmissionAttempt
    fields = (
        "repository_url",
        "comment",
        "game_version",
        "modding_environment",
        "submitted_at",
        "reviewer",
        "review_started_at",
    )
    raw_id_fields = ("reviewer",)
    extra = 0


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "exercise", "status", "created_at")
    list_filter = ("status", "enrollment__course")
    search_fields = ("enrollment__user__email", "exercise__title")
    list_select_related = ("enrollment__user", "enrollment__course", "exercise")
    raw_id_fields = ("enrollment",)
    inlines = (SubmissionAttemptInline,)


class ReviewScoreInline(admin.TabularInline):
    model = ReviewScore
    fields = ("criterion", "level")
    raw_id_fields = ("criterion",)
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Para consultar y corregir; los tutores revisan en su pantalla, no aquí."""

    list_display = ("attempt", "reviewer", "decision", "reviewed_at")
    list_filter = ("decision", "attempt__submission__enrollment__course")
    search_fields = (
        "attempt__submission__enrollment__user__email",
        "attempt__submission__exercise__title",
        "reviewer__email",
    )
    list_select_related = (
        "attempt__submission__enrollment__user",
        "attempt__submission__exercise",
        "reviewer",
    )
    raw_id_fields = ("attempt", "reviewer")
    inlines = (ReviewScoreInline,)


@admin.register(PublicationChecklist)
class PublicationChecklistAdmin(admin.ModelAdmin):
    """Solo lectura: lo completa el alumno al entregar el proyecto final."""

    list_display = ("attempt", "readme", "license", "changelog", "publication_url")
    list_filter = ("readme", "license", "changelog")
    search_fields = ("attempt__submission__enrollment__user__email", "publication_url")
    list_select_related = ("attempt__submission__enrollment__user",)
    raw_id_fields = ("attempt",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
