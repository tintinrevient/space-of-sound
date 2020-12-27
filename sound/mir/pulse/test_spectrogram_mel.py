import librosa.display
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import os

infile = os.path.join('data', 'looperman-l-2843733-0226183-glitchy-drum-loop.wav')

y, sr = librosa.load(infile)

n_mels = 128
n_fft = 2048
hop_length = 512
mel = librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=n_mels)

plt.figure(figsize=(15, 4))
plt.subplot(1, 2, 1)
librosa.display.specshow(mel, sr=sr, hop_length=hop_length, x_axis='linear')
plt.ylabel('Mel filter')
plt.colorbar()
plt.title('1. Our filter bank for converting from Hz to mels.')

plt.subplot(1, 2, 2)
mel_10 = librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=10)
librosa.display.specshow(mel_10, sr=sr, hop_length=hop_length, x_axis='linear')
plt.ylabel('Mel filter')
plt.colorbar()
plt.title('2. Easier to see what is happening with only 10 mels.')

S = np.abs(librosa.stft(y))

plt.show()

plt.plot(S[:, 1]);
plt.plot(mel.dot(S[:, 1]));
plt.legend(labels=['Hz', 'mel']);
plt.title('One sampled window for example, before and after converting to mel.');

plt.show()