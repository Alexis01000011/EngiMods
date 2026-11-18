from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Cohort, LiveSession


class LiveSessionInline(admin.TabularInline):
    model = LiveSession
    fields = ("date", "start_time", "topic", "join_url")
    extra = 0


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "start_date", "end_date", "capacity", "seats", "status")
    list_filter = ("status", "course__game", "course")
    search_fields = ("name", "course__title", "course__game__name")
    list_select_related = ("course__game",)
    filter_horizontal = ("tutors",)
    date_hierarchy = "start_date"
    inlines = (LiveSessionInline,)
    fields = (
        "course",
        "name",
        ("start_date", "end_date"),
        "capacity",
        "tutors",
        "discord_url",
        "status",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("enrollments")

    @admin.display(description=_("ocupados"))
    def seats(self, cohort):
        return f"{cohort.seats_taken} / {cohort.capacity}"


@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ("topic", "cohort", "date", "start_time")
    list_filter = ("cohort__course", "cohort")
    search_fields = ("topic", "cohort__name", "cohort__course__title")
    list_select_related = ("cohort__course",)
    date_hierarchy = "date"
