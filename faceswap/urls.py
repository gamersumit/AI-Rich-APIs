from django.urls import path
from . import views

urlpatterns = [
    path('', views.FaceSwapperAPIView.as_view(), name = 'faceswap')
]
