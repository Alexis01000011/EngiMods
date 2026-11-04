from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Course, Exercise, Lesson, LessonTest, Module


class ModuleInline(admin.TabularInline):
    model = Module
    fields = ("order", "title")
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "game", "kind", "level", "status", "price_mxn", "access_days")
    list_filter = ("status", "kind", "level", "game")
    search_fields = ("title", "slug", "game__name")
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ("game",)
    inlines = (ModuleInline,)

    @admin.display(description=_("precio (MXN)"), ordering="price_cents")
    def price_mxn(self, course):
        pesos, cents = divmod(course.price_cents, 100)
        return f"{pesos:,}.{cents:02d}"


class LessonTestInline(admin.TabularInline):
    model = LessonTest
    fields = ("game_version", "modding_environment", "tested_on")
    extra = 1


class ExerciseInline(admin.StackedInline):
    model = Exercise
    fields = ("title", "instructions")
    extra = 0


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "status", "estimated_minutes")
    list_filter = ("status", "module__course")
    search_fields = ("title", "module__title", "module__course__title")
    list_select_related = ("module__course",)
    inlines = (LessonTestInline, ExerciseInline)
