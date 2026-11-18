from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts.models import PrivacyConsent
from accounts.permissions import has_tutor_access, tutor_required
from catalog.models import Game, LabGuide, LabStep
from core.models import LegalText
from courses.models import Course, Lesson

from .forms import WaitlistJoinForm
from .models import Enrollment, LabStepProgress, LessonProgress, WaitlistEntry


def course_lessons(course):
    """Lecciones publicadas del curso, en el mismo orden que la navegación entre lecciones."""
    return list(
        Lesson.objects.published()
        .filter(module__course=course)
        .order_by("module__order", "module__pk", "order", "pk")
    )


def add_progress(enrollment):
    """Agrega a la inscripción su porcentaje de avance y la siguiente lección pendiente."""
    lessons = course_lessons(enrollment.course)
    done = set(enrollment.lesson_progress.values_list("lesson_id", flat=True))
    completed = sum(1 for lesson in lessons if lesson.pk in done)
    enrollment.completed_count = completed
    enrollment.lesson_count = len(lessons)
    # Se redondea hacia abajo: 100 % solo cuando están todas.
    enrollment.progress_percent = completed * 100 // len(lessons) if lessons else 0
    enrollment.all_done = bool(lessons) and completed == len(lessons)
    enrollment.has_lessons = bool(lessons)
    # Si el curso volvió a borrador, sus lecciones dan 404: no se enlaza ninguna.
    enrollment.next_lesson = None
    if enrollment.course.status == Course.Status.PUBLISHED:
        enrollment.next_lesson = next((item for item in lessons if item.pk not in done), None)


@login_required
def my_courses(request):
    """Panel del alumno: sus cursos con acceso vigente y los vencidos, solo los propios."""
    enrollments = Enrollment.objects.filter(
        user=request.user, status=Enrollment.Status.ACTIVE
    ).select_related("course__game__lab_guide")
    active = list(enrollments.with_access().order_by("-enrolled_at", "-pk"))

    # Un curso con una inscripción vigente no aparece también como vencido, ni se repite.
    expired = []
    seen = {enrollment.course_id for enrollment in active}
    for enrollment in enrollments.filter(access_ends_at__lte=timezone.now()).order_by(
        "-access_ends_at", "-pk"
    ):
        if enrollment.course_id not in seen:
            seen.add(enrollment.course_id)
            expired.append(enrollment)

    for enrollment in active + expired:
        add_progress(enrollment)

    catalog = []
    if not active and not expired:
        catalog = Course.objects.published().select_related("game").order_by("title")
    return render(
        request,
        "enrollments/my_courses.html",
        {"active": active, "expired": expired, "catalog": catalog},
    )


def join_waitlist(request):
    """Deja un correo para el próximo grupo o para un juego sin curso (EM-046).

    Sin aviso de privacidad vigente no se muestra el formulario ni se guarda nada.
    No crea cuenta, no inicia sesión y no envía correo.
    """
    privacy_notice = LegalText.objects.current(LegalText.Kind.PRIVACY)
    form = None
    if privacy_notice is not None:
        # El enlace de la página de un juego (EM-012) preselecciona ese juego.
        initial = {}
        game_slug = request.GET.get("juego")
        if game_slug:
            game = Game.objects.filter(status=Game.Status.ACTIVE, slug=game_slug).first()
            if game is not None:
                initial["game"] = game
        form = WaitlistJoinForm(request.POST or None, initial=initial)
        if request.method == "POST" and form.is_valid():
            with transaction.atomic():
                WaitlistEntry.objects.create(
                    email=form.cleaned_data["email"],
                    game=form.cleaned_data["game"],
                    course=form.cleaned_data["course"],
                    legal_text=privacy_notice,
                )
                PrivacyConsent.objects.create(
                    email=form.cleaned_data["email"], legal_text=privacy_notice
                )
            messages.success(
                request,
                _(
                    "Listo. Guardamos tu correo. Te avisaremos cuando abra el próximo "
                    "grupo o el curso que te interesa."
                ),
            )
            return redirect("waitlist:join")
    return render(
        request,
        "enrollments/waitlist.html",
        {"form": form, "privacy_notice": privacy_notice},
    )


@login_required
@require_POST
def toggle_lesson(request, pk):
    """Marca o desmarca una lección como completada. Solo con acceso vigente al curso."""
    lesson = get_object_or_404(
        Lesson.objects.published().select_related("module__course"),
        pk=pk,
        module__course__status=Course.Status.PUBLISHED,
    )
    course = lesson.module.course
    enrollment = Enrollment.objects.with_access().filter(user=request.user, course=course).first()
    if enrollment is None:
        raise PermissionDenied(_("No tienes acceso vigente a este curso."))
    deleted, _deleted = LessonProgress.objects.filter(enrollment=enrollment, lesson=lesson).delete()
    if not deleted:
        LessonProgress.objects.create(enrollment=enrollment, lesson=lesson)
    return redirect("courses:lesson_detail", course.slug, lesson.pk)


def is_enrolled_in_game(user, game):
    """Alumno con acceso vigente a algún curso publicado del juego."""
    if not user.is_authenticated:
        return False
    return (
        Enrollment.objects.with_access()
        .filter(user=user, course__game=game, course__status=Course.Status.PUBLISHED)
        .exists()
    )


def has_lab_access(user, game):
    return has_tutor_access(user) or is_enrolled_in_game(user, game)


def lab_students(guide):
    """Alumnos con acceso al juego y su avance, con el primer paso pendiente."""
    steps = list(guide.steps.all())
    step_ids = [step.pk for step in steps]
    enrollments = (
        Enrollment.objects.with_access()
        .filter(course__game=guide.game, course__status=Course.Status.PUBLISHED)
        .select_related("user", "course")
        .order_by("user__display_name", "user__email")
    )
    rows = {}
    for enrollment in enrollments:
        row = rows.setdefault(
            enrollment.user_id,
            {"user": enrollment.user, "course": enrollment.course, "done": 0, "next": None},
        )
        # Si el alumno tiene varios cursos del juego, muestra el primero por nombre.
        if enrollment.course.title < row["course"].title:
            row["course"] = enrollment.course
    done_by_user = {}
    if rows and step_ids:
        for user_id, step_id in LabStepProgress.objects.filter(
            user_id__in=rows, step_id__in=step_ids
        ).values_list("user_id", "step_id"):
            done_by_user.setdefault(user_id, set()).add(step_id)
    for user_id, row in rows.items():
        done = done_by_user.get(user_id, set())
        row["done"] = len(done)
        row["total"] = len(steps)
        row["next"] = next((step for step in steps if step.pk not in done), None)
        row["finished"] = bool(steps) and row["done"] == len(steps)
    return sorted(rows.values(), key=lambda row: (row["done"], row["user"].display_name))


@login_required
def lab_guide(request, game_slug):
    """Guía de laboratorio del juego (EM-063): pasos y avance del alumno."""
    guide = get_object_or_404(
        LabGuide.objects.select_related("game", "game_version", "modding_environment"),
        game__slug=game_slug,
    )
    if not has_lab_access(request.user, guide.game):
        raise PermissionDenied(_("No tienes acceso a la guía de laboratorio de este juego."))
    steps = list(guide.steps.all())
    done_ids = set(
        LabStepProgress.objects.filter(user=request.user, step__in=steps).values_list(
            "step_id", flat=True
        )
    )
    for step in steps:
        step.done = step.pk in done_ids
    can_mark = is_enrolled_in_game(request.user, guide.game)
    return render(
        request,
        "enrollments/lab_guide.html",
        {
            "guide": guide,
            "steps": steps,
            "completed": len(done_ids),
            "can_mark": can_mark,
            "tutor_rows": lab_students(guide) if has_tutor_access(request.user) else None,
        },
    )


@login_required
@require_POST
def toggle_lab_step(request, game_slug, step_pk):
    """Marca o desmarca un paso. Solo el alumno inscrito en el juego."""
    guide = get_object_or_404(LabGuide, game__slug=game_slug)
    if not is_enrolled_in_game(request.user, guide.game):
        raise PermissionDenied(_("Solo los alumnos inscritos marcan los pasos."))
    step = get_object_or_404(LabStep, pk=step_pk, guide=guide)
    deleted, _deleted = LabStepProgress.objects.filter(user=request.user, step=step).delete()
    if not deleted:
        LabStepProgress.objects.create(user=request.user, step=step)
    return redirect("enrollments:lab_guide", guide.game.slug)


@tutor_required
def lab_guides(request):
    """Lista de guías de laboratorio para el tutor."""
    guides = (
        LabGuide.objects.select_related("game", "game_version", "modding_environment")
        .annotate(steps_count=Count("steps"))
        .order_by("game__name")
    )
    return render(request, "enrollments/lab_guides.html", {"guides": guides})
