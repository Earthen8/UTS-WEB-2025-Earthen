from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Mahasiswa

def daftar_mahasiswa(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            Mahasiswa.objects.create(
                nim=request.POST.get('nim'),
                firstname=request.POST.get('firstname'),
                lastname=request.POST.get('lastname'),
                jurusan=request.POST.get('jurusan')
            )
        elif action == 'update':
            mhs = Mahasiswa.objects.get(id=request.POST.get('id'))
            mhs.nim = request.POST.get('nim')
            mhs.firstname = request.POST.get('firstname')
            mhs.lastname = request.POST.get('lastname')
            mhs.jurusan = request.POST.get('jurusan')
            mhs.save()
        elif action == 'delete':
            Mahasiswa.objects.filter(id=request.POST.get('id')).delete()

        return redirect('daftar_mahasiswa')

    semua_mahasiswa = Mahasiswa.objects.all()
    context = {
        'mymahasiswa': semua_mahasiswa,
    }
    return render(request, 'index.html', context)