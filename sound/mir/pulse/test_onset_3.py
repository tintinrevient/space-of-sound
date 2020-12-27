import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os

infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')

y, sr = librosa.load(infile, duration=3)

oenv = librosa.onset.onset_strength(y=y, sr=sr)
times = librosa.times_like(oenv)
# Detect events without backtracking
onset_raw = librosa.onset.onset_detect(onset_envelope=oenv,
                                       backtrack=False)
onset_bt = librosa.onset.onset_backtrack(onset_raw, oenv)

S = np.abs(librosa.stft(y=y))
print("S shape:", S.shape)
rms = librosa.feature.rms(S=S)
print("RMS shape:", rms.shape)
onset_bt_rms = librosa.onset.onset_backtrack(onset_raw, rms[0])

fig, ax = plt.subplots(nrows=3, sharex=True)
librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                         y_axis='log', x_axis='time', ax=ax[0])
ax[0].label_outer()
ax[1].plot(times, oenv, label='Onset strength')
ax[1].vlines(librosa.frames_to_time(onset_raw), 0, oenv.max(), label='Raw onsets')
ax[1].vlines(librosa.frames_to_time(onset_bt), 0, oenv.max(), label='Backtracked', color='r')
ax[1].legend()
ax[1].label_outer()
ax[2].plot(times, rms[0], label='RMS')
ax[2].vlines(librosa.frames_to_time(onset_bt_rms), 0, rms.max(), label='Backtracked (RMS)', color='r')
ax[2].legend()

plt.show()