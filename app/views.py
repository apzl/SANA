from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


from . forms import AudioForm
from . models import Audio
from . serializers import AudioSerializer
from . import utils
from pathlib import Path  


class AudioViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):                     #over riding default create method
        audio_file=Audio(audio=request.FILES['audio'])              
        audio=request.FILES['audio']
        spec=utils.audio_to_spec(audio,audio_file)                        #passes audio file and filename
        i=spec[6:]                                                  #gets the spectrogram file path
        prediction=utils.predict_class(Path(spec))
        data=Audio.objects.create(audio=audio,spec=i,prediction=prediction)
        data.save()
        serializer = AudioSerializer(data)
        return Response(serializer.data)
        
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

def upload_audio(request):
    if request.method=='POST':
        form=AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio=request.FILES['audio']
            print(audio.content_type)
            if(audio.content_type[:5]!="audio"):
                return HttpResponseRedirect('/404')
            elif(audio.content_type!="audio/x-wav"):
                audio=utils.convert_to_wav(audio)
                spec=utils.audio_to_spec(Path(audio))
                audio=audio[6:]
            else:
                spec=utils.audio_to_spec(audio) 
            i=spec[6:]                           
            prediction=utils.predict_class(Path(spec))
            a=Audio(audio=audio,spec=i,prediction=prediction)
            a.save()
            return HttpResponseRedirect('/predict')
        else:
            return HttpResponseRedirect('/404')

    else:
        a=Audio()
    return render(request,'home.html',{'audio':a})

def record_audio_view(request):
    if request.method=='POST':
        audio=utils.record_audio()
        spec=utils.audio_to_spec(Path(audio))
        audio=audio[6:]
        i=spec[6:]                           
        prediction=utils.predict_class(Path(spec))
        a=Audio(audio=audio,spec=i,prediction=prediction)
        a.save()
        return HttpResponseRedirect('/predict')
    return render(request,'record.html',{})


def predict_audio(request):
    audio=Audio.objects.all().last()
    context={'audio':audio}
    return render(request,'predict.html',context)

def list_audio(request):
    audios=Audio.objects.all()
    return render(request,'list.html',{'audios':audios})

def error_view(request):
    return render(request,'404.html',{})

