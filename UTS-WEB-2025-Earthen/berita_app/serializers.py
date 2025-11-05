from rest_framework import serializers
from .models import Berita, Komentar

class BeritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Berita
        fields = ['id', 'judul', 'tanggal', 'gambar', 'isi']

class KomentarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komentar
        fields = ['id', 'nama', 'tanggal', 'isi', 'berita']