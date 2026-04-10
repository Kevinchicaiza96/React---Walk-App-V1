# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from ranking.models import UserProfile


class Command(BaseCommand):
    help = 'Resetea los puntos semanales de todos los usuarios cada lunes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--forzar',
            action='store_true',
            help='Forzar el reset aunque no sea lunes',
        )

    def handle(self, *args, **options):
        hoy = timezone.now().weekday()  # 0 = lunes
        forzar = options.get('forzar', False)

        if hoy != 0 and not forzar:
            self.stdout.write(self.style.WARNING(
                f'Hoy no es lunes (dia {hoy}). Usa --forzar para ejecutar de todas formas.'
            ))
            return

        total = UserProfile.objects.count()
        UserProfile.objects.all().update(puntos_semanales=0, dias_activos=0)

        self.stdout.write(self.style.SUCCESS(
            f'Reset semanal completado. {total} usuarios reseteados — {timezone.now().strftime("%d/%m/%Y %H:%M")}'
        ))
