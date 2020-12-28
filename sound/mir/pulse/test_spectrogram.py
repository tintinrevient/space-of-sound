import librosa.display
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import os

infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')

y, sr = librosa.load(infile)

# Invert a mel power spectrogram to audio using Griffin-Lim.
# Option 2
# D = np.abs(librosa.stft(y))**2
# M = librosa.feature.melspectrogram(S=D, sr=sr)

# Option 2
# Passing through arguments to the Mel filters
M = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                    fmax=8000)

fig, ax = plt.subplots(nrows=3, sharex=True)
M_dB = librosa.power_to_db(M, ref=np.max)
img = librosa.display.specshow(M_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=ax[0])
fig.colorbar(img, ax=ax, format='%+2.0f dB')
ax[0].set(title='Mel-frequency spectrogram')

librosa.display.specshow(librosa.power_to_db(np.abs(librosa.stft(y))),
                         x_axis='time', y_axis='log', sr=sr, fmax=8000, ax=ax[1])
ax[1].set(title='STFT spectrogram')

S = librosa.feature.inverse.mel_to_stft(M)

librosa.display.specshow(librosa.power_to_db(np.abs(S)),
                         x_axis='time', y_axis='log', sr=sr, fmax=8000, ax=ax[2])
ax[2].set(title='Mel to STFT spectrogram')

plt.show()

# griffin lim
y_stft = librosa.griffinlim(S)
sf.write('./output/griffinlim_stft.wav', y_stft, sr)

y_mel = librosa.griffinlim(M)
sf.write('./output/griffinlim_mel.wav', y_mel, sr)

# D = librosa.stft(y)
# Dh, Dp = librosa.decompose.hpss(D)
# y_harmonic = librosa.istft(Dh)
