import librosa.display
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import os

infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')

y, sr = librosa.load(infile)
print("Total samples of signal:", len(y))

# plot
fig, ax = plt.subplots(nrows=2, sharex=False)

# zero-crossing rate
zero_crossing_rate = librosa.feature.zero_crossing_rate(y, hop_length=1)
print("Zero crossing rate shape:", zero_crossing_rate.shape)
ax[0].plot(zero_crossing_rate[0])

# zero-crossings in a time-series: return np.ndarray [shape=y.shape, dtype=boolean]
zero_crossings = librosa.zero_crossings(y, pad=False)
print("Zero crossing shape:", zero_crossings.shape)
print("Total number of zero crossings:", sum(zero_crossings))

# waveform
librosa.display.waveplot(y, sr=sr)
ax[1].label_outer()

plt.show()