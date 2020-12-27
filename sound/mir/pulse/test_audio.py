import numpy as np
volume = 0.5 # range [0.0, 1.0]
sr = 44100 # sampling rate, Hz, must be integer
duration = 1.0 # in seconds, may be float
freq = 440.0 # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
# a simple sine
# y = (np.sin(2*np.pi*np.arange(sr*duration)*freq/sr)).astype(np.float32)

# additive synthesis
y1 = (np.sin(2*np.pi*(freq)*np.arange(sr*duration)/sr)).astype(np.float32)
y2 = (1/3)*(np.sin(2*np.pi*(3*freq)*np.arange(sr*duration)/sr)).astype(np.float32)
y3 = (1/5)*(np.sin(2*np.pi*(5*freq)*np.arange(sr*duration)/sr)).astype(np.float32)
y = y1+y2+y3

# soundfile
# import soundfile as sf
# sf.write('./output/sine.wav', y, sr)

# pyaudio
import pyaudio
audio = pyaudio.PyAudio()

# for paFloat32 sample, values must be in range [-1.0, 1.0]
stream = audio.open(format=pyaudio.paFloat32, channels=1, rate=sr, output=True)
# play, and it may repeat with different volume values (if done interactively)
stream.write(volume * y)
stream.stop_stream()
stream.close()

audio.terminate()

# plot the frequencies
import matplotlib.pyplot as plt
import librosa.display
fig, ax = plt.subplots(nrows=3, sharex=True)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
img = librosa.display.specshow(D, x_axis='time', y_axis='linear', ax=ax[0])
ax[0].set(title='Linear-frequency power spectrogram')
ax[0].label_outer()
librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax[1])
ax[1].set(title='Log-frequency power spectrogram')
ax[1].label_outer()
librosa.display.specshow(librosa.power_to_db(librosa.feature.melspectrogram(y=y), ref=np.max),
                         x_axis='time', y_axis='mel', ax=ax[2])
ax[2].set(title='Mel-frequency power spectrogram')
ax[2].label_outer()
fig.colorbar(img, ax=ax, format="%+2.f dB")
plt.show()

# Zooming in
# from matplotlib import pyplot as plt
n0 = 8900
n1 = 9100
plt.figure(figsize=(14, 5))
plt.plot(y[n0:n1])
plt.grid()
plt.show()

# waveplot
# import librosa
# import os
# infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')
# y_test, sr_test = librosa.load(infile)

# from matplotlib import pyplot as plt
# import librosa.display
# plt.figure(figsize=(14, 5))
# librosa.display.waveplot(y=y[n0:n1], sr=sr, x_axis='ms')
# plt.show()

# playsound
# from playsound import playsound
# playsound(infile)

# pygame
# import pygame
# import time
#
# pygame.mixer.init()
# pygame.mixer.music.load(infile)
# pygame.mixer.music.play()
# time.sleep(5)

# pyglet
# import pyglet
# music = pyglet.resource.media(infile)
# music.play()
# pyglet.app.run()