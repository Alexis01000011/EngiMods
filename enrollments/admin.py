import csv

from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone
from django.utils.translation import gettext as _

from .models import Enrollment, LessonProgress, WaitlistEntry

CSV_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def csv_safe(value):
    """Evita que una celda se interprete como fórmula al abrir el CSV."""
    text = "" if value is None else str(value)
    if text.startswith(CSV_FORMULA_PREFIXES):
        return "'" + text
    return text


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


@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    """Consulta y exportación de la lista de espera, agrupada por juego (EM-046)."""

    list_display = ("email", "game", "course", "legal_text", "created_at")
    list_display_links = None
    list_filter = ("game", "course", "legal_text")
    search_fields = ("email", "game__name", "course__title")
    list_select_related = ("game", "course", "legal_text")
    date_hierarchy = "created_at"
    ordering = ("game__name", "game__pk", "course__title", "-created_at", "-pk")
    change_list_template = "admin/enrollments/waitlistentry/change_list.html"

    def has_add_permission(self, request):
        # Los intereses los captura el formulario público, no el admin.
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        custom = [
            path(
                "agrupada/",
                self.admin_site.admin_view(self.grouped_view),
                name="enrollments_waitlistentry_grouped",
            ),
            path(
                "exportar.csv",
                self.admin_site.admin_view(self.export_csv),
                name="enrollments_waitlistentry_export",
            ),
        ]
        return custom + super().get_urls()

    def _require_view_permission(self, request):
        if not self.has_view_permission(request):
            raise PermissionDenied

    def grouped_view(self, request):
        self._require_view_permission(request)
        groups = []
        for entry in self.get_queryset(request):
            if not groups or groups[-1]["game"].pk != entry.game_id:
                groups.append({"game": entry.game, "entries": []})
            groups[-1]["entries"].append(entry)
        context = {
            **self.admin_site.each_context(request),
            "title": _("Lista de espera por juego"),
            "groups": groups,
            "opts": self.model._meta,
        }
        return TemplateResponse(request, "admin/enrollments/waitlistentry/grouped.html", context)

    def export_csv(self, request):
        self._require_view_permission(request)
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="lista-de-espera.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                _("Juego"),
                _("Curso"),
                _("Correo"),
                _("Aviso de privacidad"),
                _("Registrado el"),
            ]
        )
        for entry in self.get_queryset(request):
            writer.writerow(
                [
                    csv_safe(entry.game.name),
                    csv_safe(entry.course.title if entry.course else ""),
                    csv_safe(entry.email),
                    csv_safe(entry.legal_text.version),
                    csv_safe(timezone.localtime(entry.created_at).isoformat()),
                ]
            )
        return response
