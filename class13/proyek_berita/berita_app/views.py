from rest_framework import viewsets
from .models import Berita, Komentar
from .serializers import BeritaSerializer, KomentarSerializer
from rest_framework.filters import SearchFilter
from django.shortcuts import render, get_object_or_404

class BeritaViewSet(viewsets.ModelViewSet):
    queryset = Berita.objects.all().order_by('-tanggal')
    serializer_class = BeritaSerializer
    filter_backends = [SearchFilter]
    search_fields = ['judul', 'isi']

class KomentarViewSet(viewsets.ModelViewSet):
    queryset = Komentar.objects.all().order_by('-tanggal')
    serializer_class = KomentarSerializer

def daftar_berita(request):
    return render(request, 'berita_app/daftar_berita.html')

def detail_berita(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    daftar_komentar = berita.komentar.all().order_by('-tanggal')
    context = {
        'berita': berita,
        'daftar_komentar': daftar_komentar
    }
    
    return render(request, 'berita_app/detail_berita.html', context)