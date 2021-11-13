from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('bucket/', views.Bucket.as_view(), name='bkt-home'),
    path('bucket-delete/<str:name>/', views.BucketDeleteObject.as_view(), name='bkt-del-obj'),
    path('bucket-download/<str:name>/', views.BucketDownloadObject.as_view(), name='bkt-dow-obj'),
]
