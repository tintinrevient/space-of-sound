import librosa.display
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import os

infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')

y, sr = librosa.load(infile)

S = np.abs(librosa.stft(y))

# Decompose a feature matrix.
# By default, this is done with with non-negative matrix factorization (NMF),
# but any sklearn.decomposition-type object will work.

# Decompose a magnitude spectrogram into 8 components with NMF
# comps, acts = librosa.decompose.decompose(S, n_components=8)

# Sort components by ascending peak frequency
comps, acts = librosa.decompose.decompose(S, n_components=8, sort=True)

print("Components shape:", comps.shape)
print("Activations shape:", acts.shape)
print("Spectrum shape:", S.shape)

# Or with sparse dictionary learning
# import sklearn.decomposition
# T = sklearn.decomposition.MiniBatchDictionaryLearning(n_components=8)
# scomps, sacts = librosa.decompose.decompose(S, transformer=T, sort=True)

fig, ax = plt.subplots(nrows=1, ncols=2)
librosa.display.specshow(librosa.amplitude_to_db(comps, ref=np.max),
                         y_axis='log', ax=ax[0])
ax[0].set(title='Components')
librosa.display.specshow(acts, x_axis='time', ax=ax[1])
ax[1].set(ylabel='Components', title='Activations')

fig, ax = plt.subplots(nrows=2, sharex=True, sharey=True)
librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                         y_axis='log', x_axis='time', ax=ax[0])
ax[0].set(title='Input spectrogram')
ax[0].label_outer()
S_approx = comps.dot(acts)
img = librosa.display.specshow(librosa.amplitude_to_db(S_approx, ref=np.max),
                         y_axis='log', x_axis='time', ax=ax[1])
ax[1].set(title='Reconstructed spectrogram')
fig.colorbar(img, ax=ax, format="%+2.f dB")

plt.show()