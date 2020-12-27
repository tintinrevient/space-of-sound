import librosa.display
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import os

infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')

y, sr = librosa.load(infile)

# Compute the short-time Fourier transform
Y = librosa.stft(y)

# For display purposes, compute the log amplitude of the STFT
Ymag = librosa.amplitude_to_db(Y)

# Play with the parameters, including x_axis and y_axis
librosa.display.specshow(Ymag, sr=sr, x_axis='time', y_axis='log')

plt.show()

onset_frames = librosa.onset.onset_detect(y, sr=sr)
print("Frames shape:", onset_frames.shape)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)

clicks = librosa.clicks(times=onset_times, length=len(y))
sf.write('./output/clicks.wav', (y+clicks), sr)

# onset samples
onset_samples = librosa.frames_to_samples(onset_frames)
frame_sz = int(0.1*sr)
segments = np.array([y[i:i+frame_sz] for i in onset_samples])

def concatenate_segments(segments, sr=sr, pad_time=0.300):
    padded_segments = [np.concatenate([segment, np.zeros(int(pad_time*sr))]) for segment in segments]
    return np.concatenate(padded_segments)

concatenated_signal = concatenate_segments(segments, sr)
sf.write('./output/onset_unsorted.wav', concatenated_signal, sr)

# zero-crossing samples
zcrs = [sum(librosa.core.zero_crossings(segment)) for segment in segments]
print("Zero crossings:", zcrs)

ind = np.argsort(zcrs)
print("Zero crossings sorted by index:", ind)

concatenated_signal = concatenate_segments(segments[ind], sr)
sf.write('./output/onset_sorted.wav', concatenated_signal, sr)
