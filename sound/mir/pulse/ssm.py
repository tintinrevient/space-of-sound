import os
# infile = os.path.join('data', 'looperman-l-1593910-0234478-swing-piano.wav')
infile = os.path.join('data', 'generated_clip01.wav')

import librosa
y, sr = librosa.load(infile)
print("Audio in seconds:", float(len(y))/sr)

hop_length = 512
chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)

# Use time-delay embedding to get a cleaner recurrence matrix
chroma_stack = librosa.feature.stack_memory(chroma, n_steps=10, delay=3)

# Default
R = librosa.segment.recurrence_matrix(chroma_stack)
R_lag = librosa.segment.recurrence_to_lag(R)

# Or fix the number of nearest neighbors to 5
# R = librosa.segment.recurrence_matrix(chroma_stack, k=5)

# Suppress neighbors within +- 7 frames
# R = librosa.segment.recurrence_matrix(chroma_stack, width=7)

# Use cosine similarity instead of Euclidean distance
# R = librosa.segment.recurrence_matrix(chroma_stack, metric='cosine')

# Require mutual nearest neighbors
# R = librosa.segment.recurrence_matrix(chroma_stack, sym=True)

# Use an affinity matrix instead of binary connectivity
R_aff = librosa.segment.recurrence_matrix(chroma_stack, metric='cosine', mode='affinity')

from matplotlib import pyplot as plt
import librosa.display

fig, ax = plt.subplots(ncols=2, sharex=True, sharey=True)
img_sim = librosa.display.specshow(R, x_axis='s', y_axis='time',
                                  hop_length=hop_length, ax=ax[0])
ax[0].set(title='Binary recurrence (symmetric)')

img_aff = librosa.display.specshow(R_aff, x_axis='s', y_axis='time',
                                   hop_length=hop_length, cmap='magma_r', ax=ax[1])
ax[1].set(title='Affinity recurrence')
ax[1].label_outer()

fig.colorbar(img_sim, ax=ax[0], orientation='horizontal', ticks=[0, 1])
fig.colorbar(img_aff, ax=ax[1], orientation='horizontal')

plt.show()
