from django.db import models

class Berita(models.Model):
    judul = models.CharField(max_length=200)
    tanggal = models.DateTimeField(auto_now_add=True) 
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True) 
    isi = models.TextField()

    def __str__(self):
        return self.judul

class Komentar(models.Model):
    nama = models.CharField(max_length=100)
    tanggal = models.DateTimeField(auto_now_add=True)
    isi = models.TextField()
    berita = models.ForeignKey(
        Berita, 
        related_name='komentar', 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Komentar oleh {self.nama} di {self.berita.judul}'