from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BeritaViewSet, KomentarViewSet

router = DefaultRouter()
router.register(r'berita', BeritaViewSet)
router.register(r'komentar', KomentarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]