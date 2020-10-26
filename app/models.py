from django.db import models
from django.conf import settings
from django.utils import timezone
import os


class Audio(models.Model):
	audio = models.FileField(upload_to='audio',blank=False,null=True)
	spec = models.ImageField(upload_to='spectrogram',null=True)
	utime = models.DateTimeField(default=timezone.now)
	prediction = models.CharField(max_length=20,null=True)

	def __str__(self):
		return self.prediction	

	