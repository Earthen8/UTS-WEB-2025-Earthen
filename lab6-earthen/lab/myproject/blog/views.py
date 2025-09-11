from django.shortcuts import render
from .models import Mahasiswa
from django.template import loader
from django.http import HttpResponse

def daftar_mahasiswa(request):
    semua_mahasiswa = Mahasiswa.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'mymahasiswa': semua_mahasiswa,
        }

    return HttpResponse(template.render(context, request))