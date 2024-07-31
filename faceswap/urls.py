from django.urls import path
from . import views

urlpatterns = [
    path('', views.FaceSwapperAPIView.as_view(), name = 'faceswap'),
    path('overlay/', views.AddTextToImage.as_view(), name = 'text-overlay'),
    path('<str:pk>/', views.GetSwappedImage.as_view(), name = 'get-swapped-image'),
]
