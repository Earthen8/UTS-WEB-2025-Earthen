from django.db import models

class Mahasiswa(models.Model):
    nim = models.CharField(max_length=10, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    jurusan = models.CharField(max_length=100)

    def __str__(self):
        return self.nim