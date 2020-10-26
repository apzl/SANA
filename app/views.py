from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib import messages

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets

from . forms import AudioForm
from . models import Audio
from . serializers import AudioSerializer


from fastai import *
from fastai.vision import *

import pickle
import librosa
import librosa.display
import numpy as np
from pathlib import Path  
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram


class AudioViewSet(viewsets.ModelViewSet):
	queryset = Audio.objects.all()
	serializer_class = AudioSerializer


def upload_audio(request):
    if request.method=='POST':
        form=AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file=Audio(audio=request.FILES['audio'])
            audio=request.FILES['audio']
            spec=audio_to_spec(audio,audio_file)
            i=spec[6:]
            prediction=predict_class(Path(spec))
            a=Audio(audio=audio,spec=i,prediction=prediction)
            a.save()
            return HttpResponseRedirect('/predict')
    else:
        a=Audio()
    return render(request,'home.html',{'audio':a})
    
def predict_audio(request):
    audio=Audio.objects.all().last()
    context={'audio':audio}
    return render(request,'predict.html',context)

def list_audio(request):
    audios=Audio.objects.all()
    return render(request,'list.html',{'audios':audios})


def audio_to_spec(audio,audio_file):
    if audio:
        samples, sample_rate = librosa.load(audio)
        fig = plt.figure(figsize=[0.72,0.72])
        ax = fig.add_subplot(111)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        name  = 'media/spectrogram/'+audio_file.audio.name.replace('.wav','.png')
        S = librosa.feature.melspectrogram(y=samples, sr=sample_rate)
        librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
        plt.savefig(name, dpi=400, bbox_inches='tight',pad_inches=0)
        plt.close('all')
        return name

def predict_class(spec):
    path = Path('')
    labels  = ['air_conditioner','car_horn','children_playing','dog_bark','drilling','engine_idling','gun_shot','jackhammer','siren','street_music']
    if spec is not None:
        img=open_image(spec)
        learn=load_learner(path)
        pred=learn.predict(img)[1]
        return labels[pred]

		
		
	

	
