from decimal import Decimal

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from .models import Course, Lesson, Module


def course_detail(request, slug):
    course = get_object_or_404(Course.objects.published().select_related("game"), slug=slug)
    lessons = Prefetch("lessons", queryset=Lesson.objects.published().order_by("order", "pk"))
    modules = Module.objects.filter(course=course).order_by("order", "pk").prefetch_related(lessons)
    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "modules": modules,
            "price": Decimal(course.price_cents) / 100,
        },
    )
