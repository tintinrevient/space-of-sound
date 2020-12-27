import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os

infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')

y, sr = librosa.load(infile, duration=3)

S = np.abs(librosa.stft(y))
times = librosa.times_like(S)

print("Length of y:", len(y))
print("Times of y:", len(y)/sr)
print("Times:", times.shape)

fig, ax = plt.subplots(nrows=2, sharex=True)
librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                         y_axis='log', x_axis='time', ax=ax[0])
ax[0].set(title='Power spectrogram')
ax[0].label_outer()

onset_env = librosa.onset.onset_strength(y=y, sr=sr)
print("Onset envelop shape:", onset_env.shape)
ax[1].plot(times, 2 + onset_env / onset_env.max(), alpha=0.8,
           label='Mean (mel)')

onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                         aggregate=np.median,
                                         fmax=8000, n_mels=256)
ax[1].plot(times, 1 + onset_env / onset_env.max(), alpha=0.8,
           label='Median (custom mel)')

C = np.abs(librosa.cqt(y=y, sr=sr))
S = np.abs(librosa.stft(y=y))
print("C shape:", C.shape)
print("S shape:", S.shape)
onset_env = librosa.onset.onset_strength(sr=sr, S=librosa.amplitude_to_db(C, ref=np.max))
# onset_env = librosa.onset.onset_strength(sr=sr, S=librosa.amplitude_to_db(S, ref=np.max))
ax[1].plot(times, onset_env / onset_env.max(), alpha=0.8,
         label='Mean (CQT)')
ax[1].legend()
ax[1].set(ylabel='Normalized strength', yticks=[])

plt.show()