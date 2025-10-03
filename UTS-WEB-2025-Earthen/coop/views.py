from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MahasiswaRegistrationForm, CustomAuthenticationForm, MagangConfirmationForm, LaporanBulananForm, LaporanAkhirForm, EvaluasiSupervisorForm
from .models import Mahasiswa, Magang, Lowongan, LaporanBulanan, LaporanAkhir, EvaluasiSupervisor
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail

def register_view(request):
    if request.method == 'POST':
        form = MahasiswaRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=email).exists():
                messages.error(request, 'Email ini sudah terdaftar. Silakan login.')
                return redirect('register')

            user = User.objects.create_user(username=email, email=email, password=password)

            mahasiswa = form.save(commit=False)
            mahasiswa.user = user
            mahasiswa.email_outlook = email
            mahasiswa.save()

            messages.success(request, 'Pendaftaran berhasil! Silakan login.')
            return redirect('login')
    else:
        form = MahasiswaRegistrationForm()
        
    return render(request, 'register.html', {'form': form})

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Selamat datang kembali, {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Email atau Password Anda salah. Silakan coba lagi.")
            
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard_view(request):
    try:
        mahasiswa = Mahasiswa.objects.get(user=request.user)
    except Mahasiswa.DoesNotExist:
        messages.error(request, "Akun Anda tidak memiliki profil mahasiswa yang valid. Silakan login kembali atau registrasi ulang.")
        logout(request)
        return redirect('login')

    magang = Magang.objects.filter(mahasiswa=mahasiswa).first()

    nama_parts = mahasiswa.nama_lengkap.split()
    initials = ""
    if len(nama_parts) > 0:
        initials += nama_parts[0][0]
    if len(nama_parts) > 1:
        initials += nama_parts[1][0]

    context = {
        'mahasiswa': mahasiswa,
        'magang': magang,
        'initials': initials.upper()
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah berhasil logout.")
    return redirect('index')

@login_required
def lowongan_view(request):
    queryset = Lowongan.objects.filter(is_active=True).order_by('-posted_at')

    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(posisi__icontains=query) |
            Q(nama_perusahaan__icontains=query) |
            Q(lokasi__icontains=query) |
            Q(deskripsi__icontains=query)
        ).distinct()

    context = {
        'semua_lowongan': queryset
    }
    return render(request, 'lowongan.html', context)

@login_required
def lowongan_detail_view(request, lowongan_id):
    lowongan = get_object_or_404(Lowongan, id=lowongan_id)
    
    context = {
        'lowongan': lowongan
    }
    return render(request, 'lowongan_detail.html', context)

@login_required
def internship_reports_view(request):
    mahasiswa = get_object_or_404(Mahasiswa, user=request.user)
    magang = Magang.objects.filter(mahasiswa=mahasiswa).first()

    confirmation_form = None
    report_form = None
    semua_laporan = None

    if magang:
        if request.method == 'POST':
            report_form = LaporanBulananForm(request.POST)
            if report_form.is_valid():
                laporan = report_form.save(commit=False)
                laporan.magang = magang
                laporan.save()
                messages.success(request, "Laporan bulanan berhasil disubmit!")
                return redirect('dashboard')
        else:
            report_form = LaporanBulananForm()
        
        semua_laporan = LaporanBulanan.objects.filter(magang=magang).order_by('-created_at')

    else:
        if request.method == 'POST':
            confirmation_form = MagangConfirmationForm(request.POST, request.FILES)
            if confirmation_form.is_valid():
                new_magang = confirmation_form.save(commit=False)
                new_magang.mahasiswa = mahasiswa
                new_magang.save()

                try:
                    subjek = f"Konfirmasi Magang Baru: {mahasiswa.nama_lengkap} ({mahasiswa.nim})"
                    pesan = f"""
                    Mahasiswa berikut telah berhasil melakukan konfirmasi magang:

                    Nama    : {mahasiswa.nama_lengkap}
                    NIM     : {mahasiswa.nim}
                    Prodi   : {mahasiswa.get_program_studi_display()}

                    Perusahaan: {new_magang.nama_perusahaan}
                    Posisi    : {new_magang.posisi}
                    Periode   : {new_magang.tanggal_mulai.strftime('%d %B %Y')} s/d {new_magang.tanggal_selesai.strftime('%d %B %Y')}
                    """
                    send_mail(
                        subjek, pesan, 'sistem-coop@prasetiyamulya.ac.id',
                        ['kaprodi@prasetiyamulya.ac.id', 'mentor@prasetiyamulya.ac.id'],
                        fail_silently=False,
                    )
                    messages.success(request, "Konfirmasi magang berhasil disimpan dan notifikasi telah dikirim.")
                except Exception as e:
                    messages.success(request, "Konfirmasi magang berhasil disimpan.")
                    messages.warning(request, f"Namun, notifikasi email gagal dikirim. Error: {e}")
                
                return redirect('dashboard')
        else:
            confirmation_form = MagangConfirmationForm()

    context = {
        'magang': magang,
        'confirmation_form': confirmation_form,
        'report_form': report_form,
        'semua_laporan': semua_laporan
    }

    return render(request, 'laporan.html', context)

@login_required
def laporan_detail_view(request, laporan_id):
    laporan = get_object_or_404(LaporanBulanan, id=laporan_id, magang__mahasiswa__user=request.user)
    
    context = {
        'laporan': laporan
    }
    return render(request, 'laporan_detail.html', context)

@login_required
def laporan_akhir_view(request):
    try:
        magang = Magang.objects.get(mahasiswa__user=request.user)
        if LaporanAkhir.objects.filter(magang=magang).exists():
            messages.warning(request, "Anda sudah pernah mengumpulkan laporan akhir.")
            return redirect('dashboard')
    except Magang.DoesNotExist:
        messages.error(request, "Anda harus melakukan konfirmasi magang terlebih dahulu.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = LaporanAkhirForm(request.POST, request.FILES)
        if form.is_valid():
            laporan = form.save(commit=False)
            laporan.magang = magang
            laporan.save()
            messages.success(request, "Laporan akhir Anda berhasil disimpan!")
            return redirect('dashboard')
    else:
        form = LaporanAkhirForm()

    context = {'form': form}
    return render(request, 'laporan_akhir.html', context)

@login_required
def sertifikat_view(request):
    try:
        magang = Magang.objects.get(mahasiswa__user=request.user)
    except Magang.DoesNotExist:
        messages.error(request, "Sertifikat hanya tersedia setelah Anda menyelesaikan program magang.")
        return redirect('dashboard')

    context = {
        'magang': magang,
        'mahasiswa': magang.mahasiswa,
    }
    return render(request, 'sertifikat.html', context)

def evaluasi_supervisor_view(request, token):
    evaluasi = get_object_or_404(EvaluasiSupervisor, token=token)

    if evaluasi.sudah_diisi:
        return render(request, 'evaluasi_sukses.html', {'pesan': 'Anda sudah pernah mengisi form evaluasi ini sebelumnya. Terima kasih.'})

    if request.method == 'POST':
        form = EvaluasiSupervisorForm(request.POST, instance=evaluasi)
        if form.is_valid():
            eval_instance = form.save(commit=False)
            eval_instance.sudah_diisi = True
            eval_instance.tanggal_diisi = timezone.now()
            eval_instance.save()
            return render(request, 'evaluasi_sukses.html', {'pesan': 'Terima kasih banyak telah mengisi form evaluasi.'})
    else:
        form = EvaluasiSupervisorForm(instance=evaluasi)

    context = {
        'form': form,
        'evaluasi': evaluasi
    }
    return render(request, 'evaluasi_form.html', context)