from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Mahasiswa, GENDER_CHOICES, Magang, LaporanBulanan, LaporanAkhir, EvaluasiSupervisor

class MahasiswaRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nim@student.prasetiyamulya.ac.id'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    jenis_kelamin = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True, label="Jenis Kelamin")

    class Meta:
        model = Mahasiswa
        fields = ['nama_lengkap', 'nim', 'program_studi', 'angkatan', 'jenis_kelamin', 'kontak_whatsapp', 'bukti_konsultasi', 'sptjm', 'cv', 'portfolio']
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Earthen Krisdian Setya'}),
            'nim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 23502410009'}),
            'program_studi': forms.Select(attrs={'class': 'form-select'}),
            'angkatan': forms.Select(attrs={'class': 'form-select'}),
            'kontak_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 081234567890'}),
            'bukti_konsultasi': forms.FileInput(attrs={'class': 'form-control'}),
            'sptjm': forms.FileInput(attrs={'class': 'form-control'}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
            'portfolio': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Outlook Email Address:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nim@student.prasetiyamulya.ac.id', 'autocomplete': 'email'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password', 'autocomplete': 'current-password'}))

class MagangConfirmationForm(forms.ModelForm):
    class Meta:
        model = Magang
        fields = ['tanggal_mulai', 'tanggal_selesai', 'posisi', 'nama_perusahaan', 'alamat_perusahaan', 'bidang_usaha', 'nama_supervisor', 'email_supervisor', 'kontak_supervisor', 'bukti_konfirmasi']
        widgets = {
            'tanggal_mulai': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Pilih tanggal mulai'}),
            'tanggal_selesai': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Pilih tanggal selesai'}),
            'posisi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Data Analyst Intern'}),
            'nama_perusahaan': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat_perusahaan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bidang_usaha': forms.Select(attrs={'class': 'form-select'}),
            'nama_supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            'email_supervisor': forms.EmailInput(attrs={'class': 'form-control'}),
            'kontak_supervisor': forms.TextInput(attrs={'class': 'form-control'}),
            'bukti_konfirmasi': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LaporanBulananForm(forms.ModelForm):
    class Meta:
        model = LaporanBulanan
        fields = ['profil_perusahaan', 'jobdesk', 'suasana_kerja', 'manfaat_perkuliahan', 'kesenjangan_pembelajaran']
        widgets = {
            'profil_perusahaan': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'jobdesk': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'suasana_kerja': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'manfaat_perkuliahan': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'kesenjangan_pembelajaran': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class LaporanAkhirForm(forms.ModelForm):
    class Meta:
        model = LaporanAkhir
        fields = ['kesimpulan_magang', 'dokumen_laporan_akhir']
        widgets = {
            'kesimpulan_magang': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'dokumen_laporan_akhir': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EvaluasiSupervisorForm(forms.ModelForm):
    class Meta:
        model = EvaluasiSupervisor
        fields = ['penilaian_kinerja', 'penilaian_komunikasi', 'masukan_tambahan']
        widgets = {
            'penilaian_kinerja': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'penilaian_komunikasi': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'masukan_tambahan': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }