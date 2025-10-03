from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('laporan/', views.internship_reports_view, name='internship_reports'),
    path('lowongan/', views.lowongan_view, name='lowongan'),
    path('lowongan/<int:lowongan_id>/', views.lowongan_detail_view, name='lowongan_detail'),
    path('laporan/detail/<int:laporan_id>/', views.laporan_detail_view, name='laporan_detail'),
    path('laporan/akhir/', views.laporan_akhir_view, name='laporan_akhir'),
    path('sertifikat/', views.sertifikat_view, name='sertifikat'),
    path('evaluasi/<uuid:token>/', views.evaluasi_supervisor_view, name='isi_evaluasi'),
]