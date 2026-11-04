from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from courses.models import Course

from .models import Enrollment


@login_required
def my_courses(request):
    """Panel del alumno: sus cursos con acceso vigente y los vencidos, solo los propios."""
    enrollments = Enrollment.objects.filter(
        user=request.user, status=Enrollment.Status.ACTIVE
    ).select_related("course")
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

    catalog = []
    if not active and not expired:
        catalog = Course.objects.published().select_related("game").order_by("title")
    return render(
        request,
        "enrollments/my_courses.html",
        {"active": active, "expired": expired, "catalog": catalog},
    )
