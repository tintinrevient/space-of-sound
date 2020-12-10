# Import our favorite libraries
import librosa
import mir_eval
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

infile = os.path.join('data', 'thomas.flac')
power_spec_outfile = os.path.join('pix', 'power_spec_thomas.png')
stft_spec_outfile = os.path.join('pix', 'stft_spec_thomas.png')

# Ask for a sorted list of all audio files in this subdirectory
# audio_files = librosa.util.find_files(os.path.join('data'))

# And the same thing for beats. Beat annotations are .txt files here
# beat_files = librosa.util.find_files(os.path.join(os.environ['HOME'], 'data', 'beatles_iso', 'beat'), ext='txt')

# track = audio_files[0]
track = infile

# Which song is it?
print(os.path.basename(track))

# First thing: load in the audio.
# By default, this will resample to sr=22050 Hz.
y, sr = librosa.load(track)

# There was a request from the audience to show a spectrogram visualization
# Here we get the Mel-scaled power spectrogram from the audio input
power_spec_out = librosa.feature.melspectrogram(y=y, sr=sr)

# the STFT spectrogram of the audio
window_size = 1024
window = np.hanning(window_size)
hop_length = 512
stft_spect_out  = librosa.core.spectrum.stft(y=y, n_fft=window_size, hop_length=hop_length, window=window)
stft_spect_out = 2 * np.abs(stft_spect_out) / np.sum(window)

# specshow is a wrapper to matplotlib's imshow
# we use logamplitude to scale the values in a more perceptually-friendly way
# we only show the first 1000 columns for clarity on the projector
# ref_power is the reference power against with log power (dB) is measured; in this case, the max in the spectrogram

# for plotting headlessly
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

fig = plt.Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)

# stft spec
p = librosa.display.specshow(librosa.amplitude_to_db(stft_spect_out[:,:1000], ref=np.max), ax=ax, y_axis='log', x_axis='time')
fig.savefig(stft_spec_outfile)

# power spec
p = librosa.display.specshow(librosa.power_to_db(power_spec_out[:,:1000]), ax=ax, y_axis='log', x_axis='time')
fig.savefig(power_spec_outfile)

# Now let's get the tempo and beat events from the audio
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

# We can print out the frame numbers...
print(beats[:10])

# Or we can print out the frame timings
# frame<->time conversion depends on the sampling rate, hop length, and window size of the STFT.
# These constants are the defaults used by the beat tracker, as described in the documentation
beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=64, n_fft=2048)

# Print out the times corresponding to the frame numbers above
print(beat_times[:10])

# How good did we do?  Let's use mir_eval to import the ground truth annotation
# true_beat = mir_eval.io.load_events(beat_files[7])[0]

# Print the true beats
# print(true_beat[:10])

# Doug Eck's favorite beat metric is F-measure, so we print it here.
# mir_eval.beat.f_measure(true_beat, beat_times)