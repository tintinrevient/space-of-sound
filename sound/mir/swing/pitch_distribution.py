import glob
import os
import music21
import pretty_midi
import librosa
import matplotlib.pyplot as plt
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


def plot_pitch_distribution(indir, outfile):

    # Initialize the pitch histogram with 0 for all 88 keys in pitch_midi [21, 108]
    pitch_hist = {pitch_midi: 0 for pitch_midi in np.arange(start=21, stop=109, step=1)}

    for infile in glob.glob(os.path.join(indir, '*.mid')):

        print('Infile:', infile)

        try:
            # Get the midi data
            midi_data = pretty_midi.PrettyMIDI(infile)

            for instrument in midi_data.instruments:
                if not instrument.is_drum:
                    for note in instrument.notes:
                        pitch_midi = note.pitch
                        # pitch_note = librosa.midi_to_note(pitch_midi)

                        # If pitch_midi is not in valid range [21, 108], skip it!!!
                        if pitch_midi not in pitch_hist.keys():
                            continue

                        # Update the pitch histogram
                        pitch_count = pitch_hist[pitch_midi]
                        pitch_count += 1

                        pitch_hist.update({pitch_midi: pitch_count})
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

    # Histogram
    plt.bar(np.arange(88), pitch_hist.values());
    plt.xticks(np.arange(88), [librosa.midi_to_note(pitch_midi) for pitch_midi in np.arange(start=21, stop=109, step=1)], rotation='vertical')
    plt.xlabel('Note')
    plt.ylabel('Proportion')
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

    # Musescore: 64 files
    # indir = os.path.join('midis_final_selection', 'musescore_swing_pianos')
    # outdir = os.path.join('midis_final_selection', 'musescore_swing_pianos_c')
    # outfile = os.path.join('plots', 'musescore_swing_pianos_c_pitch_distribution.png')

    # Swing pianos: 53 files
    # indir = os.path.join('midis_final_selection', 'swing_pianos_top_5_tags')
    # outdir = os.path.join('midis_final_selection', 'swing_pianos_top_5_tags_c')
    # outfile = os.path.join('plots', 'swing_pianos_top_5_tags_c_pitch_distribution.png')

    # Jazz pianos top 5: 739 files
    # indir = os.path.join('midis_final_selection', 'jazz_pianos_top_5_tags')
    # outdir = os.path.join('midis_final_selection', 'jazz_pianos_top_5_tags_c')
    # outfile = os.path.join('plots', 'jazz_pianos_top_5_tags_c_pitch_distribution.png')

    # Musescore: 64 files + Swing pianos: 53 files = 117 files
    outdir = outdir = os.path.join('midis_final_selection', 'swing_pianos_c')
    outfile = os.path.join('plots', 'swing_pianos_c_pitch_distribution.png')

    # Step 1 - Transpose to C
    # transpose_to_c(indir=indir, outdir=outdir)

    # Step 2 - Plot the pitch distribution
    plot_pitch_distribution(indir=outdir, outfile=outfile)