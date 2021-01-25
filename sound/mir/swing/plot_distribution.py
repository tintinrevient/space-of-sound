import glob
import os
import music21
from music21 import *
import pretty_midi
import librosa
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

def transpose_to_c(indir, outdir):

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for infile in glob.glob(os.path.join(indir, '*.mid')):

        print('Infile:', infile)

        # Original key
        score = music21.converter.parse(infile)
        key = score.analyze('key')
        print('Original key:', key)

        # Transpose key to C major / minor
        interval = music21.interval.Interval(key.tonic, music21.pitch.Pitch('C'))
        transposed_score = score.transpose(interval)
        transposed_key = transposed_score.analyze('key')
        print('Transposed key:', transposed_key)

        # Save the transposed score as midi file
        outfile = os.path.join(outdir, infile.split('/')[-1])
        print('Outfile:', outfile)
        transposed_score.write('midi', outfile)


def plot_pitch_distribution(indir_train, indir_generated, outfile):

    # Initialize the pitch histogram with 0 for all 88 keys in pitch_midi [21, 108]
    pitch_hist_train = {pitch_midi: 0 for pitch_midi in np.arange(start=21, stop=109, step=1)}
    pitch_hist_generated = {pitch_midi: 0 for pitch_midi in np.arange(start=21, stop=109, step=1)}

    for infile in glob.glob(os.path.join(indir_train, '*.mid')):

        print('Infile (Train):', infile)

        try:
            # Get the midi data
            midi_data = pretty_midi.PrettyMIDI(infile)

            for instrument in midi_data.instruments:
                if not instrument.is_drum:
                    for note in instrument.notes:
                        pitch_midi = note.pitch
                        # pitch_note = librosa.midi_to_note(pitch_midi)

                        # If pitch_midi is not in valid range [21, 108], skip it!!!
                        if pitch_midi not in pitch_hist_train.keys():
                            continue

                        # Update the pitch histogram
                        pitch_count = pitch_hist_train[pitch_midi]
                        pitch_count += 1

                        pitch_hist_train.update({pitch_midi: pitch_count})
        except:
            # mido.midifiles.meta.KeySignatureError: Could not decode key with 10 flats and mode 0
            pass

    for infile in glob.glob(os.path.join(indir_generated, '*.mid')):

        print('Infile (Generated):', infile)

        try:
            # Get the midi data
            midi_data = pretty_midi.PrettyMIDI(infile)

            for instrument in midi_data.instruments:
                if not instrument.is_drum:
                    for note in instrument.notes:
                        pitch_midi = note.pitch
                        # pitch_note = librosa.midi_to_note(pitch_midi)

                        # If pitch_midi is not in valid range [21, 108], skip it!!!
                        if pitch_midi not in pitch_hist_generated.keys():
                            continue

                        # Update the pitch histogram
                        pitch_count = pitch_hist_generated[pitch_midi]
                        pitch_count += 1

                        pitch_hist_generated.update({pitch_midi: pitch_count})
        except:
            # mido.midifiles.meta.KeySignatureError: Could not decode key with 10 flats and mode 0
            pass

    # Histogram inverted
    # plt.rcdefaults()
    # fig, ax = plt.subplots()
    # ax.barh(np.arange(88), pitch_hist.values(), align='center')
    # ax.set_yticks(np.arange(88))
    # ax.set_yticklabels([librosa.midi_to_note(pitch_midi) for pitch_midi in np.arange(start=21, stop=109, step=1)])
    # ax.invert_yaxis()
    # ax.set_xlabel('Proportion')
    # plt.show()

    # Convert from absolute count to percentage
    pitch_hist_train_total_count = sum(pitch_hist_train.values())
    for (key, value) in pitch_hist_train.items():
        pitch_hist_train.update({key: (value/pitch_hist_train_total_count)})

    pitch_hist_generated_total_count = sum(pitch_hist_generated.values())
    for (key, value) in pitch_hist_generated.items():
        pitch_hist_generated.update({key: (value/pitch_hist_generated_total_count)})

    # Histogram
    index = np.arange(88)
    width = np.min(np.diff(index))/3 # the width of the bars

    plt.bar(index, pitch_hist_train.values(), width, label='Training');
    plt.bar(index + width, pitch_hist_generated.values(), width, label='Generated');

    plt.xticks(index + width/2, (librosa.midi_to_note(pitch_midi) for pitch_midi in np.arange(start=21, stop=109, step=1)), rotation='vertical')
    plt.legend(loc='best')
    # plt.xlabel('Note')
    # plt.ylabel('Proportion')
    plt.subplots_adjust(bottom=0.15)

    # Get current figure
    figure = plt.gcf()
    # Set the ratio
    figure.set_size_inches(16, 9)

    # Save the figure
    plt.savefig(outfile, dpi=100)
    # Display the figure for the testing
    # plt.show()


def plot_pitch_class_distribution(indir_train, indir_generated, outfile):

    # Initialize the pitch class labels of all 12 classes
    pitch_class_labels = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')

    # Initialize the pitch class histogram
    pitch_class_hist_train = np.zeros(12)
    pitch_class_hist_generated = np.zeros(12)

    for infile in glob.glob(os.path.join(indir_train, '*.mid')):

        print('Infile (Train):', infile)

        try:
            # Get the midi data
            midi_data = pretty_midi.PrettyMIDI(infile)

            for instrument in midi_data.instruments:
                # Only piano
                if not instrument.is_drum and len(midi_data.instruments) == 1:
                    num_of_notes = len(instrument.notes)
                    midi_data_pitch_class_hist = midi_data.get_pitch_class_histogram()
                    midi_data_pitch_class_hist = midi_data_pitch_class_hist * num_of_notes

            # Update the pitch class histogram
            pitch_class_hist_train = pitch_class_hist_train + np.array(midi_data_pitch_class_hist)

        except:
            # mido.midifiles.meta.KeySignatureError: Could not decode key with 10 flats and mode 0
            pass

    for infile in glob.glob(os.path.join(indir_generated, '*.mid')):

        print('Infile (Generated):', infile)

        try:
            # Get the midi data
            midi_data = pretty_midi.PrettyMIDI(infile)

            for instrument in midi_data.instruments:
                # Only piano
                if not instrument.is_drum and len(midi_data.instruments) == 1:
                    num_of_notes = len(instrument.notes)
                    midi_data_pitch_class_hist = midi_data.get_pitch_class_histogram()
                    midi_data_pitch_class_hist = midi_data_pitch_class_hist * num_of_notes

            # Update the pitch class histogram
            pitch_class_hist_generated = pitch_class_hist_generated + np.array(midi_data_pitch_class_hist)

        except:
            # mido.midifiles.meta.KeySignatureError: Could not decode key with 10 flats and mode 0
            pass

    # Convert from absolute count to percentage
    pitch_class_hist_train_total_count = sum(pitch_class_hist_train)
    pitch_class_hist_train = [value/pitch_class_hist_train_total_count for value in pitch_class_hist_train]

    pitch_class_hist_generated_total_count = sum(pitch_class_hist_generated)
    pitch_class_hist_generated = [value/pitch_class_hist_generated_total_count for value in pitch_class_hist_generated]

    # Histogram
    index = np.arange(12)
    width = np.min(np.diff(index)) / 3  # the width of the bars

    plt.bar(index, pitch_class_hist_train, width, label='Training');
    plt.bar(index + width, pitch_class_hist_generated, width, label='Generated');

    plt.xticks(index + width / 2, pitch_class_labels)
    plt.legend(loc='best')
    # plt.xlabel('Pitch Class')
    # plt.ylabel('Proportion')
    plt.subplots_adjust(bottom=0.15)

    # Get current figure
    figure = plt.gcf()
    # Set the ratio
    figure.set_size_inches(16, 9)

    # Save the figure
    plt.savefig(outfile, dpi=100)
    # Display the figure for the testing
    # plt.show()


def plot_mode_distribution(indir_train, indir_generated, outfile):

    # Initialize the mode histogram
    mode_hist_train = {}
    mode_hist_generated = {}

    for infile in glob.glob(os.path.join(indir_train, '*.mid')):

        print('Infile (Train):', infile)

        try:
            # Get the midi data
            midi_data = pretty_midi.PrettyMIDI(infile)

            # Original key
            score = music21.converter.parse(infile)
            key = str(score.analyze('key'))
            print('Original key:', key)

            if key not in mode_hist_train.keys():
                mode_hist_train.update({key: 1})
            else:
                key_count = mode_hist_train.get(key)
                key_count += 1
                mode_hist_train.update({key: key_count})

        except:
            # mido.midifiles.meta.KeySignatureError: Could not decode key with 10 flats and mode 0
            pass

    for infile in glob.glob(os.path.join(indir_generated, '*.mid')):

        print('Infile (Generated):', infile)

        try:
            # Get the midi data
            midi_data = pretty_midi.PrettyMIDI(infile)

            # Original key
            score = music21.converter.parse(infile)
            key = str(score.analyze('key'))
            print('Original key:', key)

            if key not in mode_hist_generated.keys():
                mode_hist_generated.update({key: 1})
            else:
                key_count = mode_hist_generated.get(key)
                key_count += 1
                mode_hist_generated.update({key: key_count})

        except:
            # mido.midifiles.meta.KeySignatureError: Could not decode key with 10 flats and mode 0
            pass

    # Convert from absolute count to percentage
    total_keys = list(set(mode_hist_train.keys()) | set(mode_hist_generated.keys()))
    mode_hist_train_total = {}
    mode_hist_generated_total = {}

    mode_hist_train_total_count = sum(mode_hist_train.values())
    for key in total_keys:
        if key in mode_hist_train.keys():
            mode_hist_train_total.update({key: (mode_hist_train.get(key)/mode_hist_train_total_count)})
        else:
            mode_hist_train_total.update({key: 0.0})

    mode_hist_generated_total_count = sum(mode_hist_generated.values())
    for key in total_keys:
        if key in mode_hist_generated.keys():
            mode_hist_generated_total.update({key: (mode_hist_generated.get(key)/mode_hist_generated_total_count)})
        else:
            mode_hist_generated_total.update({key: 0.0})

    # Histogram
    index = np.arange(len(total_keys))
    width = np.min(np.diff(index)) / 3  # the width of the bars

    plt.bar(index, mode_hist_train_total.values(), width, label='Training');
    plt.bar(index + width, mode_hist_generated_total.values(), width, label='Generated');

    plt.xticks(index + width / 2, total_keys, rotation='vertical')
    plt.legend(loc='best')
    # plt.xlabel('Pitch Class')
    # plt.ylabel('Proportion')
    plt.subplots_adjust(bottom=0.15)

    # Get current figure
    figure = plt.gcf()
    # Set the ratio
    figure.set_size_inches(16, 9)

    # Save the figure
    plt.savefig(outfile, dpi=100)
    # Display the figure for the testing
    # plt.show()


def plot_meter_distribution(indir_train, indir_generated, outfile):

    # Initialize the meter histogram
    meter_hist_train = {}
    meter_hist_generated = {}

    for infile in glob.glob(os.path.join(indir_train, '*.mid')):

        print('Infile:', infile)

        try:
            # Get the midi data
            midi_data = midi.MidiFile()
            midi_data.open(infile)
            midi_data.read()
            midi_data.close()

            stream_data = midi.translate.midiFileToStream(midi_data)
            time_signature = stream_data.getTimeSignatures()[0]

            # Test
            meter = str(time_signature.beatCount) + '/' + str(time_signature.denominator)

            if meter not in meter_hist_train.keys():
                meter_hist_train.update({meter: 1})
            else:
                meter_count = meter_hist_train.get(meter)
                meter_count += 1
                meter_hist_train.update({meter: meter_count})

        except:
            # mido.midifiles.meta.KeySignatureError: Could not decode key with 10 flats and mode 0
            pass

    for infile in glob.glob(os.path.join(indir_generated, '*.mid')):

        print('Infile:', infile)

        try:
            # Get the midi data
            midi_data = midi.MidiFile()
            midi_data.open(infile)
            midi_data.read()
            midi_data.close()

            stream_data = midi.translate.midiFileToStream(midi_data)
            time_signature = stream_data.getTimeSignatures()[0]

            # Test
            meter = str(time_signature.beatCount) + '/' + str(time_signature.denominator)

            if meter not in meter_hist_generated.keys():
                meter_hist_generated.update({meter: 1})
            else:
                meter_count = meter_hist_generated.get(meter)
                meter_count += 1
                meter_hist_generated.update({meter: meter_count})

        except:
            # mido.midifiles.meta.KeySignatureError: Could not decode key with 10 flats and mode 0
            pass

    # Convert from absolute count to percentage
    total_keys = list(set(meter_hist_train.keys()) | set(meter_hist_generated.keys()))
    meter_hist_train_total = {}
    meter_hist_generated_total = {}

    meter_hist_train_total_count = sum(meter_hist_train.values())
    for key in total_keys:
        if key in meter_hist_train.keys():
            meter_hist_train_total.update({key: (meter_hist_train.get(key) / meter_hist_train_total_count)})
        else:
            meter_hist_train_total.update({key: 0.0})

    meter_hist_generated_total_count = sum(meter_hist_generated.values())
    for key in total_keys:
        if key in meter_hist_generated.keys():
            meter_hist_generated_total.update(
                {key: (meter_hist_generated.get(key) / meter_hist_generated_total_count)})
        else:
            meter_hist_generated_total.update({key: 0.0})

    # Histogram
    index = np.arange(len(total_keys))
    width = np.min(np.diff(index)) / 3  # the width of the bars

    plt.bar(index, meter_hist_train_total.values(), width, label='Training');
    plt.bar(index + width, meter_hist_generated_total.values(), width, label='Generated');

    plt.xticks(index + width / 2, total_keys)
    plt.legend(loc='best')
    # plt.xlabel('Pitch Class')
    # plt.ylabel('Proportion')
    plt.subplots_adjust(bottom=0.15)

    # Get current figure
    figure = plt.gcf()
    # Set the ratio
    figure.set_size_inches(16, 9)

    # Save the figure
    plt.savefig(outfile, dpi=100)
    # Display the figure for the testing
    # plt.show()


if __name__ == '__main__':

    # Training
    # Musescore: 64 files + Swing pianos: 53 files + Jazz pianos top 5: 739 files = 815 files (duplicates)
    indir_train = os.path.join('midis_final_selection', 'pianos')
    outdir_train = os.path.join('midis_final_selection', 'pianos_c')

    # Generated
    indir_generated = os.path.join('generated_new', 'piano_2_bar')
    outdir_generated = os.path.join('generated_new', 'piano_2_bar_c')

    # Plot files
    outfile_pitch = os.path.join('plots', 'pianos_c_pitch_distribution.png')
    outfile_pitch_class = os.path.join('plots', 'pianos_c_pitch_class_distribution.png')
    outfile_mode = os.path.join('plots', 'pianos_mode_distribution.png')
    outfile_meter = os.path.join('plots', 'pianos_meter_distribution.png')

    # Step 1 - Transpose to C
    # transpose_to_c(indir=indir, outdir=outdir)

    # Step 2 - Plot the pitch distribution
    # plot_pitch_distribution(indir_train=outdir_train, indir_generated=outdir_generated, outfile=outfile_pitch)

    # Step 3 - Plot the pitch class distribution
    # plot_pitch_class_distribution(indir_train=outdir_train, indir_generated=outdir_generated, outfile=outfile_pitch_class)

    # Step 4 - Plot the mode distribution
    # plot_mode_distribution(indir_train=indir_train, indir_generated=indir_generated, outfile=outfile_mode)

    # Step 5 - Plot the meter distribution
    plot_meter_distribution(indir_train=outdir_train, indir_generated=outdir_generated, outfile=outfile_meter)

    # Debugging ...
    # Test for "Chambermaid Swing" from Parov Stelar
    # infile = os.path.join('entire_song_midis', 'all_musescore_swings_full_tracks', 'full_104206.mid')

    # Get the midi data
    # midi_data = pretty_midi.PrettyMIDI(infile)

    # Original key
    # score = music21.converter.parse(infile)
    # key = str(score.analyze('key'))
    # print('Original key:', key)