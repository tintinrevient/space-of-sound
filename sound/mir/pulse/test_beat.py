import librosa
import librosa.display
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import os

infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')

y, sr = librosa.load(infile)
# y, sr = sf.read(infile)

# Now let's get the tempo and beat events from the audio
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=512)
print("Number of notes:", len(y))

print("Number of beats:", len(beats))
print(beats)

print("Tempo:", tempo)

# Or we can print out the frame timings
# frame<->time conversion depends on the sampling rate, hop length, and window size of the STFT.
# These constants are the defaults used by the beat tracker, as described in the documentation
# beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=64, n_fft=2048)
beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=512)

# Print out the times corresponding to the frame numbers above
print("Number of beat times:", len(beat_times))
print(beat_times)

# Predominant local pulse (PLP) estimation
pulse = librosa.beat.plp(y=y, sr=sr)
print("Number of pulse:", len(pulse))
print(pulse[20:80])

cqt = np.abs(librosa.cqt(y, sr=sr, hop_length=512))
subseg = librosa.segment.subsegment(cqt, beats, n_segments=2)
subseg_t = librosa.frames_to_time(subseg, sr=sr, hop_length=512)

fig, ax = plt.subplots()
librosa.display.specshow(librosa.amplitude_to_db(cqt,
                                                 ref=np.max),
                         y_axis='cqt_hz', x_axis='time', ax=ax)
lims = ax.get_ylim()
ax.vlines(beat_times, lims[0], lims[1], color='lime', alpha=0.9,
           linewidth=2, label='Beats')
ax.vlines(subseg_t, lims[0], lims[1], color='linen', linestyle='--',
           linewidth=1.5, alpha=0.5, label='Sub-beats')
ax.legend()
ax.set(title='CQT + Beat and sub-beat markers')

plt.show()