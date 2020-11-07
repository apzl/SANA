from django.urls import path, include
from . import views
from .views import AudioViewSet
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'app', views.AudioViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls',namespace='rest_framework')),
	path('home/',views.upload_audio,name='upload_audio'),
    path('list/',views.list_audio,name='list_audio'),
    path('predict/',views.predict_audio,name='predict_audio'),
    path('record/',views.record_audio_view,name='record_audio'),
    path('404/',views.error_view,name='error')

 
] 