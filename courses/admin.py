from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .models import Course, Exercise, Lesson, LessonTest, Module, RubricCriterion


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
    # La rúbrica se captura en la página del ejercicio.
    show_change_link = True


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "status", "estimated_minutes")
    list_filter = ("status", "module__course")
    search_fields = ("title", "module__title", "module__course__title")
    list_select_related = ("module__course",)
    inlines = (LessonTestInline, ExerciseInline)


class RubricCriterionInline(admin.TabularInline):
    model = RubricCriterion
    fields = ("order", "title", "description")
    extra = 1


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """La rúbrica se captura aquí, criterio por criterio (EM-072)."""

    list_display = ("title", "lesson", "course", "criteria_count")
    list_filter = ("lesson__module__course",)
    search_fields = ("title", "lesson__title", "lesson__module__course__title")
    list_select_related = ("lesson__module__course",)
    raw_id_fields = ("lesson",)
    inlines = (RubricCriterionInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(criteria_count=Count("rubric_criteria"))

    @admin.display(description=_("curso"), ordering="lesson__module__course__title")
    def course(self, exercise):
        return exercise.lesson.module.course

    @admin.display(description=_("criterios"), ordering="criteria_count")
    def criteria_count(self, exercise):
        return exercise.criteria_count
