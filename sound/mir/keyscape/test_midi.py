from midi2audio import FluidSynth

FluidSynth().midi_to_audio('./data/fugue_c_major_bwv846.mid', './data/fugue_c_major_bwv846.wav')
# FluidSyntbaltimor.midh().play_midi('baltimor.mid')


# https://pypi.org/project/midi2audio/

# pip install midi2audio
# brew install fluidsynth

# play MIDI
# $ midiplay input.mid

# synthesize MIDI to audio
# $ midi2audio input.mid output.wav

# also to FLAC
# $ midi2audio input.mid output.flac

# MP3 to wav
# ffmpeg -i foo.mp3 -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav foo.wav