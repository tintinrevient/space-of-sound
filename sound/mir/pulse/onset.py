import os
infile = os.path.join('data', 'looperman-l-1593910-0234478-swing-piano.wav')

import librosa
y, sr = librosa.load(infile)
print("Audio in seconds:", float(len(y))/sr)

# onset envelope in times
hop_length = 512
oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
times = librosa.times_like(oenv, sr=sr, hop_length=hop_length)

# onset envelope --> onset_detect in times
# onset_frames = librosa.onset.onset_detect(onset_envelope=oenv, sr=sr, units='time')
onset_frames = librosa.onset.onset_detect(onset_envelope=oenv, sr=sr)

# onset envelope --> beat_track in times
tempo, beat_frames = librosa.beat.beat_track(onset_envelope=oenv)
# beat_times = librosa.frames_to_time(beat_frames, sr=sr)

from matplotlib import pyplot as plt
# onset envelope in times
fig, ax = plt.subplots(nrows=1, figsize=(10, 10), sharex=True, sharey=True)
ax.plot(times, oenv, label='Onset strength')

# onset detect in times
ax.plot(times[onset_frames], oenv[onset_frames], 'ro', markersize=5, label='Detected note onsets')

# beat_track in times
lims = ax.get_ylim()
ax.vlines(times[beat_frames], lims[0], lims[1],
          color='lime', alpha=0.9, linewidth=1, linestyle='--', label='Detected beats')

ax.label_outer()
ax.legend(frameon=True)

plt.show()