from decimal import Decimal

from django.conf import settings
from django.db.models import Count, Prefetch, Q
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from catalog.models import Game, GameVersion
from courses.models import Course, Lesson, LessonTest

from .models import LegalText


def latest_tests(courses):
    """La prueba más reciente de las lecciones publicadas de cada curso, por id de curso."""
    tests = (
        LessonTest.objects.filter(
            lesson__module__course__in=courses, lesson__status=Lesson.Status.PUBLISHED
        )
        .select_related("game_version", "modding_environment", "lesson__module")
        .order_by("-tested_on", "-pk")
    )
    latest = {}
    for test in tests:
        latest.setdefault(test.lesson.module.course_id, test)
    return latest


def home(request):
    """Landing (EM-040): propuesta de valor, cursos publicados y juegos activos."""
    courses = list(Course.objects.published().select_related("game").order_by("title", "pk"))
    # Primero las prácticas cortas (Misión Cero), que son la puerta de entrada.
    courses.sort(key=lambda course: course.kind != Course.Kind.SHORT_PRACTICE)
    tests = latest_tests(courses)
    for course in courses:
        course.price = Decimal(course.price_cents) / 100
        course.latest_test = tests.get(course.pk)
    practices = [c for c in courses if c.kind == Course.Kind.SHORT_PRACTICE]
    group_courses = [c for c in courses if c.kind == Course.Kind.COURSE]
    current_versions = Prefetch(
        "versions", queryset=GameVersion.objects.filter(is_current=True), to_attr="current"
    )
    games = (
        Game.objects.filter(status=Game.Status.ACTIVE)
        .annotate(
            published_courses=Count("courses", filter=Q(courses__status=Course.Status.PUBLISHED))
        )
        .prefetch_related(current_versions)
    )
    return render(
        request,
        "core/home.html",
        {
            "courses": courses,
            "practices": practices,
            "group_courses": group_courses,
            "games": games,
            "review_hours": settings.REVIEW_DEADLINE_HOURS,
        },
    )


def health(request):
    """Chequeo simple para el servidor de despliegue."""
    return JsonResponse({"status": "ok"})


def privacy(request):
    """Aviso de privacidad vigente. El texto se captura en el admin (LegalText)."""
    legal_text = LegalText.objects.current(LegalText.Kind.PRIVACY)
    if legal_text is None:
        raise Http404(_("Todavía no hay un aviso de privacidad vigente."))
    return render(request, "core/legal_text.html", {"legal_text": legal_text})


def terms(request):
    """Términos y política de devolución vigentes. El texto se captura en el admin (LegalText)."""
    legal_text = LegalText.objects.current(LegalText.Kind.TERMS)
    if legal_text is None:
        raise Http404(_("Todavía no hay términos y condiciones vigentes."))
    return render(request, "core/legal_text.html", {"legal_text": legal_text})
