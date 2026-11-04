from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "game", "kind", "level", "status", "price_mxn", "access_days")
    list_filter = ("status", "kind", "level", "game")
    search_fields = ("title", "slug", "game__name")
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ("game",)

    @admin.display(description=_("precio (MXN)"), ordering="price_cents")
    def price_mxn(self, course):
        pesos, cents = divmod(course.price_cents, 100)
        return f"{pesos:,}.{cents:02d}"
