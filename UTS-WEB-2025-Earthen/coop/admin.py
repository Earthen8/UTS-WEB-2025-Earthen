import csv
from django.http import HttpResponse
from django.contrib import admin, messages
from django.urls import reverse
from django.core.mail import send_mail
from .models import Mahasiswa, Magang, LaporanBulanan, Lowongan, EvaluasiSupervisor, LaporanAkhir

def export_evaluasi_as_csv(modeladmin, request, queryset):
    field_names = ['mahasiswa', 'nim', 'perusahaan', 'penilaian_kinerja', 'penilaian_komunikasi', 'masukan_tambahan', 'sudah_diisi', 'tanggal_diisi']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=evaluasi_supervisor.csv'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for evaluasi in queryset:
        writer.writerow([
            evaluasi.magang.mahasiswa.nama_lengkap,
            evaluasi.magang.mahasiswa.nim,
            evaluasi.magang.nama_perusahaan,
            evaluasi.penilaian_kinerja,
            evaluasi.penilaian_komunikasi,
            evaluasi.masukan_tambahan,
            evaluasi.sudah_diisi,
            evaluasi.tanggal_diisi
        ])
    return response
export_evaluasi_as_csv.short_description = "Download Laporan Evaluasi Terpilih (CSV)"

def kirim_form_evaluasi(modeladmin, request, queryset):
    for magang in queryset:
        evaluasi, created = EvaluasiSupervisor.objects.get_or_create(magang=magang)
        link_evaluasi = request.build_absolute_uri(
            reverse('isi_evaluasi', args=[evaluasi.token])
        )
        
        subjek = f"Formulir Evaluasi Kinerja Magang untuk {magang.mahasiswa.nama_lengkap}"
        pesan = f"""
        Yth. Bapak/Ibu {magang.nama_supervisor},

        Terima kasih atas kesediaan Anda dalam membimbing mahasiswa kami, {magang.mahasiswa.nama_lengkap}, 
        selama periode magang di {magang.nama_perusahaan}.

        Sebagai bagian dari evaluasi program, kami mohon kesediaan Anda untuk mengisi formulir evaluasi kinerja melalui link unik di bawah ini.

        Link Evaluasi: {link_evaluasi}
        
        Terima kasih atas kerja sama Anda.

        Hormat kami,
        Tim COOP Universitas Prasetiya Mulya
        """
        
        try:
            send_mail(
                subjek, pesan, 'coop@prasetiyamulya.ac.id',
                [magang.email_supervisor], fail_silently=False,
            )
            modeladmin.message_user(request, f"Email evaluasi untuk {magang.mahasiswa.nama_lengkap} telah 'dikirim' ke terminal.", messages.SUCCESS)
        except Exception as e:
            modeladmin.message_user(request, f"Gagal mengirim email untuk {magang.mahasiswa.nama_lengkap}: {e}", messages.ERROR)
kirim_form_evaluasi.short_description = "Kirim Formulir Evaluasi ke Supervisor"

class EvaluasiSupervisorAdmin(admin.ModelAdmin):
    list_display = ('get_nama_mahasiswa', 'get_nama_perusahaan', 'sudah_diisi', 'tanggal_diisi')
    list_filter = ('sudah_diisi',)
    search_fields = ('magang__mahasiswa__nama_lengkap', 'magang__nama_perusahaan')
    actions = [export_evaluasi_as_csv]

    def get_nama_mahasiswa(self, obj):
        return obj.magang.mahasiswa.nama_lengkap
    get_nama_mahasiswa.short_description = 'Nama Mahasiswa'

    def get_nama_perusahaan(self, obj):
        return obj.magang.nama_perusahaan
    get_nama_perusahaan.short_description = 'Perusahaan'

class MagangAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'nama_perusahaan', 'posisi')
    search_fields = ('mahasiswa__nama_lengkap', 'nama_perusahaan')
    actions = [kirim_form_evaluasi]

if admin.site.is_registered(Mahasiswa):
    admin.site.unregister(Mahasiswa)

if admin.site.is_registered(Magang):
    admin.site.unregister(Magang)
admin.site.register(Magang, MagangAdmin)

if admin.site.is_registered(EvaluasiSupervisor):
    admin.site.unregister(EvaluasiSupervisor)
admin.site.register(EvaluasiSupervisor, EvaluasiSupervisorAdmin)

if not admin.site.is_registered(LaporanBulanan):
    admin.site.register(LaporanBulanan)
if not admin.site.is_registered(Lowongan):
    admin.site.register(Lowongan)
if not admin.site.is_registered(LaporanAkhir):
    admin.site.register(LaporanAkhir)