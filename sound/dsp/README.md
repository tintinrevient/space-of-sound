# DSP

## Code Snippet

### Sin Tone

```
y = sin(2*pi*440/44100*[0:44099])

sound(y, 44100)
```

### Amplitude Envolope and ADSR

```
[x, fs] = audioread('NSynthTryOut.wav'); % read wave file
xReverse = flipud(x); % flip the array up -> down

sound(xReverse, fs)

audiowrite('NSynthTryOutReverse.wav', xReverse, fs)
```

### Window

```
[x, fs] = audioread('NSynthTryOut.wav'); % read wave file 
xWindowed = x(1:500);

sound(xWindowed, fs);
```

### Up-sampling and Down-sampling

```
[x, fs] = audioread('NSynthTryOut.wav'); % read wave file 

% up-sampling
sound(upsample(x, 2), fs)

% down-sampling
sound(downsample(x, 2), fs)
```

## References