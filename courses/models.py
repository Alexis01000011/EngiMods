from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.markdown import render_markdown


def tested_outside_game(tests, game_id):
    """True si alguna prueba usa una versión o un entorno de otro juego."""
    same_game = tests.filter(game_version__game_id=game_id, modding_environment__game_id=game_id)
    return tests.exclude(pk__in=same_game).exists()


class CourseQuerySet(models.QuerySet):
    def published(self):
        """Cursos que pueden aparecer en páginas públicas."""
        return self.filter(status=Course.Status.PUBLISHED)


class Course(models.Model):
    """Práctica corta o curso por grupos de un juego. Precio y acceso son datos del admin."""

    class Kind(models.TextChoices):
        SHORT_PRACTICE = "short_practice", _("Práctica corta")
        COURSE = "course", _("Curso")

    class Level(models.TextChoices):
        BEGINNER = "beginner", _("Principiante")
        INTERMEDIATE = "intermediate", _("Intermedio")

    class Status(models.TextChoices):
        DRAFT = "draft", _("Borrador")
        PUBLISHED = "published", _("Publicado")

    title = models.CharField(_("título"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    # PROTECT: un juego con cursos se oculta, no se borra.
    game = models.ForeignKey(
        "catalog.Game",
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name=_("juego"),
    )
    kind = models.CharField(
        _("tipo"),
        max_length=20,
        choices=Kind,
        help_text=_(
            "Práctica corta: autoguiada, sin grupo, fechas ni cupo. Curso: se imparte por grupos."
        ),
    )
    level = models.CharField(_("nivel"), max_length=20, choices=Level)
    description = models.TextField(_("descripción"))
    requirements = models.TextField(_("requisitos"))
    duration_weeks = models.PositiveSmallIntegerField(
        _("duración en semanas"), validators=[MinValueValidator(1)]
    )
    price_cents = models.PositiveIntegerField(
        _("precio en centavos"),
        help_text=_("En MXN. Por ejemplo, 10000 son MXN 100.00."),
    )
    access_days = models.PositiveSmallIntegerField(
        _("días de acceso"),
        validators=[MinValueValidator(1)],
        help_text=_(
            "En una práctica corta se cuentan desde la inscripción; en un curso, "
            "desde que termina el grupo."
        ),
    )
    status = models.CharField(_("estado"), max_length=10, choices=Status, default=Status.DRAFT)

    objects = CourseQuerySet.as_manager()

    class Meta:
        ordering = ("title", "pk")
        verbose_name = _("curso")
        verbose_name_plural = _("cursos")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.pk and self.game_id:
            tests = LessonTest.objects.filter(lesson__module__course_id=self.pk)
            if tested_outside_game(tests, self.game_id):
                raise ValidationError(
                    {"game": _("El curso tiene lecciones probadas con versiones de otro juego.")}
                )


class Module(models.Model):
    """Parte de un curso; en un curso por grupos, normalmente una por semana."""

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules", verbose_name=_("curso")
    )
    title = models.CharField(_("título"), max_length=200)
    order = models.PositiveSmallIntegerField(
        _("orden"), help_text=_("Los módulos se muestran de menor a mayor.")
    )

    class Meta:
        ordering = ("course__title", "order", "pk")
        verbose_name = _("módulo")
        verbose_name_plural = _("módulos")

    def __str__(self):
        return f"{self.course} · {self.title}"

    def clean(self):
        super().clean()
        if self.pk and self.course_id:
            tests = LessonTest.objects.filter(lesson__module_id=self.pk)
            if tested_outside_game(tests, self.course.game_id):
                raise ValidationError(
                    {"course": _("El módulo tiene lecciones probadas con versiones de otro juego.")}
                )


class LessonQuerySet(models.QuerySet):
    def published(self):
        """Lecciones que pueden ver los alumnos; las de borrador no se muestran."""
        return self.filter(status=Lesson.Status.PUBLISHED)


class Lesson(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Borrador")
        PUBLISHED = "published", _("Publicada")

    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons", verbose_name=_("módulo")
    )
    title = models.CharField(_("título"), max_length=200)
    content = models.TextField(
        _("contenido"),
        help_text=_("En Markdown. Al mostrarse se quitan los scripts y el HTML inseguro."),
    )
    estimated_minutes = models.PositiveSmallIntegerField(
        _("duración estimada en minutos"), validators=[MinValueValidator(1)]
    )
    order = models.PositiveSmallIntegerField(
        _("orden"), help_text=_("Las lecciones se muestran de menor a mayor dentro del módulo.")
    )
    status = models.CharField(_("estado"), max_length=10, choices=Status, default=Status.DRAFT)

    objects = LessonQuerySet.as_manager()

    class Meta:
        ordering = ("module__course__title", "module__order", "order", "pk")
        verbose_name = _("lección")
        verbose_name_plural = _("lecciones")

    def __str__(self):
        return self.title

    @property
    def content_html(self):
        return render_markdown(self.content)

    def clean(self):
        super().clean()
        if self.pk and self.module_id:
            if tested_outside_game(self.tests.all(), self.module.course.game_id):
                raise ValidationError(
                    {"module": _("La lección se probó con versiones de otro juego.")}
                )


class LessonTest(models.Model):
    """Probado con: versión del juego y entorno de modding con los que se probó una lección."""

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="tests", verbose_name=_("lección")
    )
    # PROTECT: no se borra una versión ni un entorno con los que se probó una lección.
    game_version = models.ForeignKey(
        "catalog.GameVersion",
        on_delete=models.PROTECT,
        related_name="lesson_tests",
        verbose_name=_("versión del juego"),
    )
    modding_environment = models.ForeignKey(
        "catalog.ModdingEnvironment",
        on_delete=models.PROTECT,
        related_name="lesson_tests",
        verbose_name=_("entorno de modding"),
    )
    tested_on = models.DateField(_("fecha de prueba"))

    class Meta:
        ordering = ("-tested_on", "-pk")
        verbose_name = _("prueba de la lección")
        verbose_name_plural = _("probado con")

    def __str__(self):
        environment = self.modding_environment
        return f"{self.game_version} · {environment.name} {environment.version} ({self.tested_on})"

    def clean(self):
        super().clean()
        lesson = getattr(self, "lesson", None)
        if lesson is None or not lesson.module_id:
            return
        game_id = lesson.module.course.game_id
        errors = {}
        if self.game_version_id and self.game_version.game_id != game_id:
            errors["game_version"] = _("Elige una versión del juego del curso.")
        if self.modding_environment_id and self.modding_environment.game_id != game_id:
            errors["modding_environment"] = _("Elige un entorno de modding del juego del curso.")
        if errors:
            raise ValidationError(errors)


class Exercise(models.Model):
    """Ejercicio entregable de una lección. El alumno lo entrega con el enlace a su repositorio."""

    lesson = models.OneToOneField(
        Lesson, on_delete=models.CASCADE, related_name="exercise", verbose_name=_("lección")
    )
    title = models.CharField(_("título"), max_length=200)
    instructions = models.TextField(
        _("instrucciones"),
        help_text=_("En Markdown. Al mostrarse se quitan los scripts y el HTML inseguro."),
    )

    class Meta:
        ordering = ("lesson__module__course__title", "lesson__module__order", "lesson__order")
        verbose_name = _("ejercicio")
        verbose_name_plural = _("ejercicios")

    def __str__(self):
        return self.title

    @property
    def instructions_html(self):
        return render_markdown(self.instructions)
