from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Solo lectura: los pagos los crean el Checkout (EM-042) y el webhook (EM-043)."""

    list_display = ("user", "course", "status", "amount_cents", "created_at")
    list_filter = ("status", "course")
    search_fields = ("user__email", "user__display_name", "stripe_checkout_session_id")
    list_select_related = ("user", "course")
    readonly_fields = (
        "user",
        "course",
        "status",
        "amount_cents",
        "stripe_checkout_session_id",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
