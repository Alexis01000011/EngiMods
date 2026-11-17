"""Métricas del piloto (EM-091). Solo lectura: no tiene modelos propios (docs/arquitectura.md).

Todos los números son agregados por curso; ninguno identifica a una persona.
"""

import csv
from collections import defaultdict

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from courses.models import Course, Lesson
from enrollments.models import Enrollment, LessonProgress
from payments.models import Payment
from submissions.models import Review


def percent(part, total):
    """Porcentaje con un decimal, o None si no hay base para calcularlo."""
    return round(part * 100 / total, 1) if total else None


def account_metrics():
    """Cuentas de alumnos: sin equipo (staff, superusuarios ni tutores)."""
    students = get_user_model().objects.filter(is_staff=False, is_superuser=False, is_tutor=False)
    return {
        "registered": students.count(),
        "verified": students.filter(email_verified_at__isnull=False).count(),
    }


def course_metrics():
    """Una fila por curso con sus métricas. Cuenta solo inscripciones no canceladas."""
    # Primero las prácticas cortas, como en la landing.
    courses = list(Course.objects.select_related("game").order_by("game__name", "-kind", "title"))
    kinds = {course.pk: course.kind for course in courses}

    enrollments = list(
        Enrollment.objects.filter(status=Enrollment.Status.ACTIVE).values_list(
            "pk", "user_id", "course_id", "origin"
        )
    )
    by_course = defaultdict(list)
    for enrollment in enrollments:
        by_course[enrollment[2]].append(enrollment)
    # Quienes tienen una inscripción en algún curso por grupos.
    group_students = {
        user for _, user, course, _ in enrollments if kinds[course] == Course.Kind.COURSE
    }

    # Lecciones publicadas por curso, como en Mi panel (enrollments.views.course_lessons).
    lessons = defaultdict(set)
    for lesson, course in Lesson.objects.published().values_list("pk", "module__course_id"):
        lessons[course].add(lesson)
    done = defaultdict(set)
    for enrollment, lesson in LessonProgress.objects.values_list("enrollment_id", "lesson_id"):
        done[enrollment].add(lesson)

    checkout_users = defaultdict(set)
    for course, user in Payment.objects.values_list("course_id", "user_id"):
        checkout_users[course].add(user)

    review_hours = defaultdict(list)
    for course, submitted_at, reviewed_at in Review.objects.values_list(
        "attempt__submission__exercise__lesson__module__course_id",
        "attempt__submitted_at",
        "reviewed_at",
    ):
        review_hours[course].append((reviewed_at - submitted_at).total_seconds() / 3600)

    rows = []
    for course in courses:
        course_enrollments = by_course[course.pk]
        total = len(course_enrollments)
        course_lessons = lessons[course.pk]
        progress = []
        if course_lessons:
            progress = [
                len(done[pk] & course_lessons) / len(course_lessons)
                for pk, *_ in course_enrollments
            ]
        students = {user for _, user, _, _ in course_enrollments}
        hours = review_hours[course.pk]
        is_practice = course.kind == Course.Kind.SHORT_PRACTICE
        rows.append(
            {
                "course": course,
                "published": course.status == Course.Status.PUBLISHED,
                "checkout_started": len(checkout_users[course.pk]),
                "enrollments": total,
                "paid": sum(
                    1 for *_, origin in course_enrollments if origin == Enrollment.Origin.STRIPE
                ),
                "conversion": (
                    percent(len(students & group_students), len(students)) if is_practice else None
                ),
                "average_progress": (
                    round(sum(progress) * 100 / len(progress), 1) if progress else None
                ),
                "completion": (
                    percent(sum(1 for value in progress if value == 1), len(progress))
                    if progress
                    else None
                ),
                "reviews": len(hours),
                "review_hours": round(sum(hours) / len(hours), 1) if hours else None,
            }
        )
    return rows


@staff_member_required
def pilot(request):
    """Vista para administradores con las métricas del piloto."""
    return render(
        request,
        "metrics/pilot.html",
        {"accounts": account_metrics(), "rows": course_metrics()},
    )


CSV_HEADER = [
    "Juego",
    "Curso",
    "Tipo",
    "Estado",
    "Iniciaron el pago",
    "Inscripciones",
    "Inscripciones pagadas",
    "Conversión a curso (%)",
    "Avance promedio (%)",
    "Tasa de finalización (%)",
    "Revisiones",
    "Tiempo medio de revisión (horas)",
]


def blank_if_none(value):
    return "" if value is None else value


@staff_member_required
def pilot_csv(request):
    """Las mismas métricas en CSV. Con BOM para que Excel lea bien los acentos."""
    filename = f"metricas-piloto-{timezone.localdate():%Y-%m-%d}.csv"
    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
    response.write("﻿")
    writer = csv.writer(response)
    writer.writerow(CSV_HEADER)
    for row in course_metrics():
        course = row["course"]
        writer.writerow(
            [
                course.game.name,
                course.title,
                course.get_kind_display(),
                course.get_status_display(),
                row["checkout_started"],
                row["enrollments"],
                row["paid"],
                blank_if_none(row["conversion"]),
                blank_if_none(row["average_progress"]),
                blank_if_none(row["completion"]),
                row["reviews"],
                blank_if_none(row["review_hours"]),
            ]
        )
    accounts = account_metrics()
    writer.writerow([])
    writer.writerow(["Cuentas de alumnos registradas", accounts["registered"]])
    writer.writerow(["Cuentas con correo verificado", accounts["verified"]])
    return response
