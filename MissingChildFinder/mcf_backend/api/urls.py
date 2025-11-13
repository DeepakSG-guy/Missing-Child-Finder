from django.urls import path
from . import views


urlpatterns = [
    path('register_child/', views.register_child, name='register_child'),
    path('upload_image/', views.upload_image, name='upload_image'),
]
