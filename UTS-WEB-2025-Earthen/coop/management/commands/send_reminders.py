from django.core.management.base import BaseCommand
from django.utils import timezone
from coop.models import Mahasiswa, Magang
import datetime

class Command(BaseCommand):
    help = 'Mencari mahasiswa yang belum konfirmasi magang setelah deadline dan mengirim reminder.'

    def handle(self, *args, **options):
        deadline = datetime.date(2025, 8, 1)
        hari_ini = timezone.now().date()

        if hari_ini > deadline:
            self.stdout.write(self.style.WARNING(f"Mengecek reminder untuk tanggal {hari_ini}... Deadline ({deadline}) sudah lewat."))

            mahasiswa_sudah_magang_ids = Magang.objects.values_list('mahasiswa_id', flat=True)

            mahasiswa_belum_magang = Mahasiswa.objects.exclude(id__in=mahasiswa_sudah_magang_ids)

            if mahasiswa_belum_magang.exists():
                self.stdout.write(self.style.SUCCESS('Menemukan mahasiswa yang perlu di-reminder:'))
                for mahasiswa in mahasiswa_belum_magang:
                    self.stdout.write(f'- Mengirim reminder ke: {mahasiswa.nama_lengkap} ({mahasiswa.email_outlook})')
            else:
                self.stdout.write(self.style.SUCCESS('Semua mahasiswa sudah melakukan konfirmasi magang. Tidak ada reminder yang perlu dikirim.'))

        else:
            self.stdout.write(self.style.SUCCESS(f"Belum melewati deadline ({deadline}). Tidak ada aksi yang dilakukan."))