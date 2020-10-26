from rest_framework import serializers
from .models import Audio

class AudioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Audio
    fields = ['audio','utime','spec','prediction']