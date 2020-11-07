from fastai import *
from fastai.vision import *

import pickle
import librosa
import librosa.display
import numpy as np
from pathlib import Path  
import matplotlib.pyplot as plt
from matplotlib.pyplot import specgram

from pydub import AudioSegment
import speech_recognition as sr	
import datetime

def audio_to_spec(audio):
    if audio:
        samples, sample_rate = librosa.load(audio)
        fig = plt.figure(figsize=[0.72,0.72])
        ax = fig.add_subplot(111)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        name  = 'media/spectrogram/'+audio.name.replace('.wav','.png')
        S = librosa.feature.melspectrogram(y=samples, sr=sample_rate)
        librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
        plt.savefig(name, dpi=400, bbox_inches='tight',pad_inches=0)        #saves spectrogram to media/spectrograms with same file name as audio
        plt.close('all')
        return name

def predict_class(spec):
    path = Path('')
    labels  = ['air_conditioner','car_horn','children_playing','dog_bark','drilling','engine_idling','gun_shot','jackhammer','siren','street_music']
    if spec is not None:
        img=open_image(spec)
        learn=load_learner(path)                                            #fast.ai method to load the model
        pred=learn.predict(img)[1]
        return labels[pred]

def convert_to_wav(filename):
    sound = AudioSegment.from_file(filename)
    dest='media/audio/'+filename.name[:-3]+'wav'
    sound.export(dest, format="wav")
    return dest
    
def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  
        #print("Say something!")
        audio = r.listen(source,phrase_time_limit=4)
    basename = "audio"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix])
    recording="media/audio/"+filename+".wav"
    with open(recording, "wb") as f:
        f.write(audio.get_wav_data())
    return recording

	
