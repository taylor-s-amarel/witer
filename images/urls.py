from django.urls import path

from . import views

urlpatterns = [
    path('', views.gif_view(), name='gif-view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)