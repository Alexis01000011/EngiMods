from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import LegalText


@admin.register(LegalText)
class LegalTextAdmin(admin.ModelAdmin):
    list_display = ("kind", "version", "effective_date", "is_current")
    list_filter = ("kind",)
    search_fields = ("version", "body")

    @admin.display(boolean=True, description=_("vigente"))
    def is_current(self, obj):
        return obj == LegalText.objects.current(obj.kind)
