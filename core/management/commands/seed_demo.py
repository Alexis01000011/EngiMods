"""Datos de ejemplo para desarrollo (EM-006).

Crea dos juegos con versiones y entornos, un curso por juego con módulos y lecciones,
y tres cuentas: un tutor y dos alumnos. Se puede correr varias veces: usa las claves
naturales de cada modelo para no duplicar nada.
"""

from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from catalog.models import Game, GameVersion, ModdingEnvironment
from courses.models import Course, Lesson, LessonTest, Module

DEMO_PASSWORD = "demo12345"

GAMES = (
    {
        "slug": "pixelforge",
        "name": "PixelForge",
        "description": "Juego de ejemplo para el taller de mods.",
        "version": "1.4",
        "release_date": date(2026, 6, 1),
        "environment": ("ForgeKit", "2.1"),
        "course_slug": "primeros-pasos-pixelforge",
        "course_title": "Primeros pasos en PixelForge",
    },
    {
        "slug": "aldea-estelar",
        "name": "Aldea Estelar",
        "description": "Juego de ejemplo con un editor de mods propio.",
        "version": "0.9",
        "release_date": date(2026, 9, 15),
        "environment": ("Estelar SDK", "0.9"),
        "course_slug": "primeros-pasos-aldea-estelar",
        "course_title": "Primeros pasos en Aldea Estelar",
    },
)

MODULES = (
    {
        "order": 1,
        "title": "Prepara tu taller",
        "lessons": (
            (
                "Instala el juego y el entorno",
                "Deja listo el juego, el loader y una carpeta de trabajo.",
            ),
            (
                "Comprueba que todo funciona",
                "Abre el juego con el entorno cargado y revisa la consola.",
            ),
        ),
    },
    {
        "order": 2,
        "title": "Tu primer mod",
        "lessons": (
            (
                "Crea la estructura del proyecto",
                "Organiza el mod con carpetas, archivo de manifiesto y control de versiones.",
            ),
            (
                "Agrega un objeto nuevo",
                "Declara un objeto, pruébalo en el juego y documenta con qué versión funciona.",
            ),
        ),
    },
)

DEMO_USERS = (
    {
        "email": "tutor@example.com",
        "display_name": "Tutora de ejemplo",
        "is_tutor": True,
    },
    {
        "email": "alumno1@example.com",
        "display_name": "Alumno de ejemplo",
        "is_tutor": False,
    },
    {
        "email": "alumno2@example.com",
        "display_name": "Alumna de ejemplo",
        "is_tutor": False,
    },
)


class Command(BaseCommand):
    help = "Crea juegos, cursos, lecciones, un tutor y dos alumnos de ejemplo para desarrollo."

    @transaction.atomic
    def handle(self, *args, **options):
        self.create_users()

        for data in GAMES:
            game = Game.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "official_url": "https://example.com/",
                    "status": Game.Status.ACTIVE,
                },
            )[0]
            version = GameVersion.objects.get_or_create(
                game=game,
                number=data["version"],
                defaults={"release_date": data["release_date"], "is_current": True},
            )[0]
            environment = ModdingEnvironment.objects.update_or_create(
                game=game,
                name=data["environment"][0],
                version=data["environment"][1],
            )[0]
            environment.compatible_versions.add(version)
            course = self.create_course(game, data)
            self.create_lessons(course, version, environment)

        self.stdout.write(
            self.style.SUCCESS(
                "Datos de ejemplo listos. Cuentas: tutor@example.com, alumno1@example.com "
                f"y alumno2@example.com; contraseña: {DEMO_PASSWORD}"
            )
        )

    def create_users(self):
        user_model = get_user_model()
        for data in DEMO_USERS:
            user, created = user_model.objects.get_or_create(
                email=data["email"],
                defaults={
                    "display_name": data["display_name"],
                    "is_tutor": data["is_tutor"],
                    "email_verified_at": timezone.now(),
                },
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save(update_fields=["password"])

    def create_course(self, game, data):
        return Course.objects.update_or_create(
            slug=data["course_slug"],
            defaults={
                "title": data["course_title"],
                "game": game,
                "kind": Course.Kind.SHORT_PRACTICE,
                "level": Course.Level.BEGINNER,
                "description": f"Práctica de ejemplo para empezar a crear mods de {game}.",
                "requirements": "Computadora con el juego instalado y programación básica.",
                "duration_weeks": 2,
                "price_cents": 10000,
                "access_days": 30,
                "status": Course.Status.PUBLISHED,
            },
        )[0]

    def create_lessons(self, course, version, environment):
        for module_data in MODULES:
            module = Module.objects.update_or_create(
                course=course,
                order=module_data["order"],
                defaults={"title": module_data["title"]},
            )[0]
            for position, (title, summary) in enumerate(module_data["lessons"], start=1):
                lesson = Lesson.objects.update_or_create(
                    module=module,
                    order=position,
                    defaults={
                        "title": title,
                        "content": f"## {title}\n\n{summary}\n\nEste texto es de ejemplo.",
                        "estimated_minutes": 15,
                        "status": Lesson.Status.PUBLISHED,
                        "is_sample": module_data["order"] == 1 and position == 1,
                    },
                )[0]
                LessonTest.objects.get_or_create(
                    lesson=lesson,
                    game_version=version,
                    modding_environment=environment,
                    defaults={"tested_on": version.release_date},
                )
