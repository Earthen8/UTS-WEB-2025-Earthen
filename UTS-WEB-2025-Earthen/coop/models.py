from django.db import models
from django.contrib.auth.models import User
import uuid

PROGRAM_STUDI_CHOICES = [
    # SBE
    ('business', 'Business'),
    ('financial_technology', 'Financial Technology'),
    ('international_marketing', 'International Marketing'),
    ('finance_and_banking', 'Finance and Banking'),
    ('branding', 'Branding'),
    ('hospitality_busines', 'Hospitality Business'),
    ('event', 'Event'),
    ('business_economics', 'Business Economics'),
    ('accounting', 'Accounting'),
    # STEM
    ('artificial_intelligence_and_robotics', 'Artificial Intelligence and Robotics'),
    ('digital_business_technology', 'Digital Business Technology'),
    ('food_business_technology', 'Food Business Technology'),
    ('business_mathematics', 'Business Mathematics'),
    ('product_design_innovation', 'Product Design Innovation'),
    ('energy_business_technology', 'Energy Business Technology'),
    # SLIS
    ('international_business_law', 'International Business Law'),
]

ANGKATAN_CHOICES = [
    (2022, '2022'),
    (2023, '2023'),
    (2024, '2024'),
    (2025, '2025'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

BIDANG_USAHA_CHOICES = [
    ('teknologi', 'Teknologi Informasi'),
    ('finance', 'Keuangan & Perbankan'),
    ('manufacturing', 'Manufaktur'),
    ('retail', 'Retail & E-commerce'),
    ('consulting', 'Konsultasi Bisnis'),
    ('fmcg', 'FMCG'),
    ('healthcare', 'Kesehatan'),
    ('education', 'Pendidikan'),
    ('other', 'Lainnya'),
]

class Mahasiswa(models.Model):
    """
    Model ini menyimpan data profil lengkap mahasiswa,
    terhubung satu-ke-satu dengan model User bawaan Django untuk autentikasi.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_lengkap = models.CharField(max_length=255)
    nim = models.CharField(max_length=11, unique=True)
    program_studi = models.CharField(max_length=100, choices=PROGRAM_STUDI_CHOICES)
    angkatan = models.IntegerField(choices=ANGKATAN_CHOICES)
    jenis_kelamin = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email_outlook = models.EmailField(unique=True)
    kontak_whatsapp = models.CharField(max_length=15)
    
    bukti_konsultasi = models.FileField(upload_to='dokumen/konsultasi/')
    sptjm = models.FileField(upload_to='dokumen/sptjm/')
    cv = models.FileField(upload_to='dokumen/cv/')
    portfolio = models.FileField(upload_to='dokumen/portfolio/', blank=True, null=True)

    def __str__(self):
        return f"{self.nama_lengkap} ({self.nim})"


class Magang(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='magang')
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    posisi = models.CharField(max_length=100)
    nama_perusahaan = models.CharField(max_length=255)
    alamat_perusahaan = models.TextField()
    bidang_usaha = models.CharField(max_length=50, choices=BIDANG_USAHA_CHOICES)
    
    nama_supervisor = models.CharField(max_length=255)
    email_supervisor = models.EmailField()
    kontak_supervisor = models.CharField(max_length=20, blank=True, null=True)
    
    bukti_konfirmasi = models.FileField(upload_to='dokumen/konfirmasi/')

    nilai_akhir = models.CharField(
        max_length=2, 
        blank=True, 
        null=True, 
        help_text="Nilai akhir yang diinput oleh admin/dosen (Contoh: A, B+, C)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mahasiswa.nama_lengkap} @ {self.nama_perusahaan}"


class LaporanBulanan(models.Model):
    magang = models.ForeignKey(Magang, on_delete=models.CASCADE, related_name='laporan')
    profil_perusahaan = models.TextField()
    jobdesk = models.TextField()
    suasana_kerja = models.TextField()
    manfaat_perkuliahan = models.TextField()
    kesenjangan_pembelajaran = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Laporan {self.magang.mahasiswa.nama_lengkap} - {self.created_at.strftime('%B %Y')}"

class Lowongan(models.Model):
    posisi = models.CharField(max_length=255)
    nama_perusahaan = models.CharField(max_length=255)
    lokasi = models.CharField(max_length=100)
    deskripsi = models.TextField()
    link_aplikasi = models.URLField(max_length=255, blank=True, null=True, help_text="Link eksternal ke halaman lamaran.")
    is_active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.posisi} di {self.nama_perusahaan}"
    
class LaporanAkhir(models.Model):
    magang = models.OneToOneField(Magang, on_delete=models.CASCADE, related_name='laporan_akhir')
    kesimpulan_magang = models.TextField(help_text="Ringkasan dan kesimpulan dari seluruh pengalaman magang Anda.")
    dokumen_laporan_akhir = models.FileField(upload_to='dokumen/laporan_akhir/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laporan Akhir - {self.magang.mahasiswa.nama_lengkap}"
    
class EvaluasiSupervisor(models.Model):
    magang = models.OneToOneField(Magang, on_delete=models.CASCADE, related_name='evaluasi')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    penilaian_kinerja = models.TextField(blank=True, null=True)
    penilaian_komunikasi = models.TextField(blank=True, null=True)
    masukan_tambahan = models.TextField(blank=True, null=True)
    sudah_diisi = models.BooleanField(default=False)
    tanggal_diisi = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Evaluasi untuk {self.magang.mahasiswa.nama_lengkap}"