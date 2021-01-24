import numpy as np
import librosa
from colour import Color
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import pyplot as plt
import music21
import pretty_midi
import os
import math


NUM_NOTES = 12
NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
INTERVALS = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'd5', 'P5', 'm6', 'M6', 'm7', 'M7']
SCALES = ['major', 'minor']
# 'Typical' pitch distributions [A, A#, B, ..., G#] for major, minor scales with tonic A,
# adapted for use with other tonal centers by rotating.
MAJOR_SCALE_PROFILE = [0.16, 0.03, 0.09, 0.03, 0.13, 0.10, 0.06, 0.14, 0.03, 0.11, 0.03, 0.09]
MINOR_SCALE_PROFILE = [0.16, 0.03, 0.09, 0.13, 0.03, 0.10, 0.06, 0.14, 0.11, 0.03, 0.09, 0.03]


# Customized color map
light_rose = '#FF00B2'
dark_rose = '#CC008F'
light_rose_code = 0.0
dark_rose_code = 0.05

light_magenta = '#FF00FF'
dark_magenta = '#FF00FF'
light_magenta_code = 0.11
dark_magenta_code = 0.14

light_violet = '#7B00FF'
dark_violet = '#6300CC'
light_violet_code = 0.17
dark_violet_code = 0.2

light_blue = '#0000FF'
dark_blue = '#0000CC'
light_blue_code = 0.32
dark_blue_code = 0.3

light_azure = '#0055FF'
dark_azure = '#0044CC'
light_azure_code = 0.39
dark_azure_code = 0.38

light_cyan = '#00FFFF'
dark_cyan = '#00CCCC'
light_cyan_code = 0.42
dark_cyan_code = 0.45

light_spring = '#00FF88'
dark_spring = '#00CC6D'
light_spring_code = 0.5
dark_spring_code = 0.53

light_green = '#00FF00'
dark_green = '#00CC00'
light_green_code = 0.6
dark_green_code = 0.62

light_chartreuse = '#6EFF00'
dark_chartreuse = '#58CC00'
light_chartreuse_code = 0.70
dark_chartreuse_code = 0.72

light_yellow = '#FFFF00'
dark_yellow = '#CCCC00'
light_yellow_code = 0.75
dark_yellow_code = 0.78

light_orange = '#FF9100'
dark_orange = '#E68200'
light_orange_code = 0.83
dark_orange_code = 0.87

light_red = '#FF0000'
dark_red = '#CC0000'
light_red_code = 0.92
dark_red_code = 0.95

black = '#000000'
black_code = 1.0

ramp_colors = [light_rose, dark_rose, light_magenta, dark_magenta, light_violet, dark_violet, light_blue, dark_blue,
               light_azure, dark_azure, light_cyan, dark_cyan, light_spring, dark_spring, light_green, dark_green,
               light_chartreuse, dark_chartreuse, light_yellow, dark_yellow, light_orange, dark_orange, light_red,
               dark_red, black]

my_cmap = LinearSegmentedColormap.from_list( 'my_cmap', [Color(color).rgb for color in ramp_colors])

# circle of fifths
KEY_COLOR_DICT = {
    'A MAJOR': light_green_code,
    'A MINOR': dark_green_code,
    'A# MAJOR': light_spring_code,
    'A# MINOR': dark_spring_code,
    'B- MAJOR': light_spring_code,
    'B- MINOR': dark_spring_code,
    'B MAJOR': light_cyan_code,
    'B MINOR': dark_cyan_code,
    'C MAJOR': light_azure_code,
    'C MINOR': dark_azure_code,
    'C# MAJOR': light_blue_code,
    'C# MINOR': dark_blue_code,
    'D- MAJOR': light_blue_code,
    'D- MINOR': dark_blue_code,
    'D MAJOR': light_violet_code,
    'D MINOR': dark_violet_code,
    'D# MAJOR': light_magenta_code,
    'D# MINOR': dark_magenta_code,
    'E- MAJOR': light_magenta_code,
    'E- MINOR': dark_magenta_code,
    'E MAJOR': light_rose_code,
    'E MINOR': dark_rose_code,
    'F MAJOR': light_red_code,
    'F MINOR': dark_red_code,
    'F# MAJOR': light_orange_code,
    'F# MINOR': dark_orange_code,
    'G- MAJOR': light_orange_code,
    'G- MINOR': dark_orange_code,
    'G MAJOR': light_yellow_code,
    'G MINOR': dark_yellow_code,
    'G# MAJOR': light_chartreuse_code,
    'G# MINOR': dark_chartreuse_code,
    'A- MAJOR': light_chartreuse_code,
    'A- MINOR': dark_chartreuse_code,
    'NULL': black_code
}


def chromagram_from_file(filename, fraction, seg_index):
    """
    Takes path FILENAME to audio file and returns the file's chromagram C (numpy array with shape=(12, t=number time samples))
    """
    y, sr = librosa.load(filename)

    # duration = librosa.get_duration(y=y, sr=sr)
    duration = len(y) / sr
    print("Total duration:", duration, "seconds.")

    # todo: approximation
    fraction_of_y = int(fraction * len(y))
    start_of_y = seg_index * fraction_of_y
    end_of_y = start_of_y + fraction_of_y

    y_frac = y[start_of_y : end_of_y]
    print("Fraction of duration:", len(y_frac)/sr, "seconds.")

    # Separate harmonic component from percussive
    y_harmonic = librosa.effects.hpss(y_frac)[0]
    # Make CQT-based chromagram using only the harmonic component to avoid pollution
    C = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
    return C


def skip_interval(root, interval):
    """
    Returns note which is INTERVAL distance away from starting note ROOT.
    """
    assert root in NOTES, "Invalid note"
    assert interval in INTERVALS, "Invalid interval"
    starting_position = NOTES.index(root)
    distance = INTERVALS.index(interval)
    return NOTES[(starting_position + distance) % NUM_NOTES]


class Key(object):
    """
    Key centered at tonal center TONIC with scale SCALE
    """
    scale_profiles = {'major': MAJOR_SCALE_PROFILE, 'minor': MINOR_SCALE_PROFILE}

    def __init__(self, tonic, scale):
        assert tonic in NOTES, "Tonal center of key must belong to NOTES"
        assert scale in SCALES, "Scale for key must belong to SCALES"
        self.tonic = tonic
        self.scale = scale

    def __str__(self):
        return ' '.join((self.tonic, self.scale))

    def __hash__(self):
        return hash(self.tonic + '_' + self.scale)

    def __repr__(self):
        return ''.join(("Key('", self.tonic, "', '", self.scale, "')"))

    def __eq__(self, other):
        if type(other) != Key:
            return False
        return self.tonic == other.tonic and self.scale == other.scale

    def get_tonic(self):
        return self.tonic

    def get_scale(self):
        return self.scale

    def get_key_profile(self):
        """
        Return typical PitchDistribution for Key
        """
        scale_profile = Key.scale_profiles[self.scale]
        key_profile = PitchDistribution()
        for i in range(NUM_NOTES):
            current_note = skip_interval(self.tonic, INTERVALS[i])
            val = scale_profile[i]
            key_profile.set_val(current_note, val)
        return key_profile


class PitchDistribution(object):
    """
    Distribution over pitch classes A, A#, ..., G, G# in the form of a map NOTES --> [0,1]
    """
    def __init__(self, values_array=None):
        """
        Initializes empty distribution.
        """
        self.distribution = {}
        if values_array:
            assert len(values_array) == NUM_NOTES, "Distribution must have %d notes, %d provided" % (NUM_NOTES, len(values_array))
            for i in range(NUM_NOTES):
                note = NOTES[i]
                val = values_array[i]
                self.set_val(note, val)
            self.normalize()

    @classmethod
    def from_file(cls, filename, fraction, seg_index):
        """
        Given path FILENAME to audio file, return its PitchDistribution
        """
        def chromagram_index_to_note(i):
            """
            Given row index in librosa chromagram, returns note it represents
            """
            return skip_interval('C', INTERVALS[i])

        C = chromagram_from_file(filename, fraction, seg_index)
        # Pick out only most prominent note in each time interval
        single_note_reduction = C.argmax(axis=0)

        dist = PitchDistribution()
        for i in np.nditer(single_note_reduction):
            note = chromagram_index_to_note(i)
            dist.increment_val(note)
        dist.normalize()
        print('Distribution:', dist)
        return dist

    def __str__(self):
        return str([(note, self.get_val(note)) for note in NOTES])

    def to_array(self):
        return [self.get_val(note) for note in NOTES]

    def set_val(self, note, val):
        self.distribution[note] = float(val)

    def get_val(self, note):
        if note in self.distribution:
            return self.distribution[note]
        return 0.0

    def increment_val(self, note):
        """
        Increments value of note NOTE in a distribution
        """
        self.set_val(note, self.get_val(note) + 1)

    def normalize(self):
        """
        Normalize distribution so that all entries sum to 1
        """
        distribution_sum = sum(self.distribution.values())
        if distribution_sum != 0:
            for note in NOTES:
                val = self.get_val(note)
                self.set_val(note, val / float(distribution_sum))


class Classifier(object):
    """
    Abstract class for classifiers PitchDistribution --> key (distributional key finders)
    """
    def __init__(self):
        if type(self) is Classifier:
            raise Exception("Classifier is an abstract class and can't be directly instantiated")

    @staticmethod
    def get_key_profiles():
        """
        Return dictionary of typical pitch class distribution for all keys
        """
        profiles = {}
        for tonic in NOTES:
            for scale in SCALES:
                key = Key(tonic, scale)
                profiles[key] = key.get_key_profile()
        return profiles

    def get_key(self, dist):
        """
        Given PitchDistribution DIST, return classifier's guess for its key
        """
        raise NotImplementedError("Subclasses of Classifier must implement get_key method")


class KrumhanslSchmuckler(Classifier):
    """
    Classifier using the Krumhansl-Schmuckler key-finding algorithm
    """
    def __init__(self):
        self.key_profiles = self.get_key_profiles()

    def correlation(self, key, dist):
        """
        Given key KEY and pitch distribution DIST, return correlation coefficient of DIST and KEY's pitch profile
        """
        key_profile = self.key_profiles[key].to_array()
        data = np.array([dist, key_profile])
        return np.corrcoef(data)[1, 0]

    def get_key(self, dist):
        """
        Given PitchDistribution DIST, return the key whose typical pitch profile best matches it
        """
        assert len(dist.distribution) == NUM_NOTES, "Distribution must have %d notes, %d provided" % (NUM_NOTES, len(dist.distribution))
        dist = dist.to_array()
        correlations = {k: self.correlation(k, dist) for k in self.key_profiles}
        return max(correlations, key=correlations.get)


class NaiveBayes(Classifier):
    """
    Classifier using a Naive Bayes model with values of a pitch distribution as features
    """
    def __init__(self):
        self.key_profiles = self.get_key_profiles()

    def get_proportion_probability(self, key, note, prop):
        """
        Return probability of a PitchDistribution with true key KEY having value PROP for note NOTE
        """
        expected_proportion = self.key_profiles[key].get_val(note)
        return 1 - (prop - expected_proportion)**2

    def get_key_likelihood(self, key, dist):
        """
        Return probability proportional to that of PitchDistribution DIST given key KEY
        """
        likelihood = 1.0
        for note in NOTES:
            likelihood *= self.get_proportion_probability(key, note, dist.get_val(note))
        return likelihood

    def get_key(self, dist):
        """
        Given PitchDistribution DIST, return the key which is most likely given Naive Bayes model
        """
        assert len(dist.distribution) == NUM_NOTES, "Distribution must have %d notes, %d provided" % (NUM_NOTES, len(dist.distribution))
        likelihoods = {k: self.get_key_likelihood(k, dist) for k in self.key_profiles}
        return max(likelihoods, key=likelihoods.get)


def estimate_key_by_naive_bayes(infile):

    naive_bayes = NaiveBayes()
    dist = PitchDistribution.from_file(
        filename=infile,
        fraction=1.,
        seg_index=0)
    key_bayes = naive_bayes.get_key(dist)  # Returns Key object Key('G', 'major')
    print("Key in Naive Bayes:", key_bayes)


def estimate_key_by_krumhansl_schmuckler_classifier(infile):

    krumhansl_schmuckler = KrumhanslSchmuckler()
    dist = PitchDistribution.from_file(
        filename=infile,
        fraction=1.,
        seg_index=0)
    key_krumhansl = krumhansl_schmuckler.get_key(dist)  # Returns Key object Key('B', 'minor')
    print("Key in Krumhansl Schumuckler Classifier:", key_krumhansl)


def plot_keyscape_from_audio(infile):

    bins = 256
    bin_size_list = [2 ** i for i in range(0, 9)]
    bin_size_list.reverse()

    krumhansl_schmuckler = KrumhanslSchmuckler()

    X = np.zeros((len(bin_size_list), bins))
    row = 0

    for bin_size in bin_size_list:
        frac = bin_size / bins
        step = int(frac * bins)

        for seg_index in range(bins // bin_size):
            print('Fraction:', frac)
            print('Start index:', seg_index)

            dist = PitchDistribution.from_file(filename=infile, fraction=frac, seg_index=seg_index)
            key = krumhansl_schmuckler.get_key(dist)
            print("Estimated key:", key)

            key_str = str(key).upper()
            print("Adjusted key:", key_str)

            key_cm_value = KEY_COLOR_DICT[key_str]
            # print("Key color value:", key_cm_value)

            start_index = seg_index * step
            end_index = start_index + step

            print('Row: %d, Start array: %d, End array: %d' % (row, start_index, end_index))

            X[row, start_index:end_index] = key_cm_value
            # print(X[row])

        row = row + 1

    span = bins // len(bin_size_list)
    X_SPANNED = np.zeros((span * len(bin_size_list), bins))
    for row_ind, row in enumerate(X):
        for col in range(span):
            X_SPANNED[row_ind * span + col] = row

    # print("Original shape:", X.shape)
    # print("Expanded shape:", X_SPANNED.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(X_SPANNED, cmap=my_cmap, vmin=0, vmax=1)

    cbar = plt.colorbar(im)
    cbar.ax.get_yaxis().set_ticks([])
    for j, lab in enumerate(['     E Major', '     E Minor', '     D# Major', '     D# Minor', '     D Major',
                             '     D Minor', '     C# Major', '     C# Minor', '     C Major', '     C Minor',
                             '     B Major', '     B Minor', '     A# Major', '     A# Minor', '     A Major',
                             '     A Minor', '     G# Major', '     G# Minor', '     G Major', '     G Minor',
                             '     F# Major', '     F# Minor', '     F Major', '     F Minor', '     NULL']):
        cbar.ax.text(0., j / 25, lab, ha='left', va='bottom')

    plt.show()
    fig.savefig('./pix/Chambermaid_Swing_Audio.png', dpi=fig.dpi)


def find_elements_in_range(elements, start_time, end_time):
    """Filters elements which are within a time range."""

    filtered_elements = []

    for item in elements:
        if hasattr(item, 'start') and hasattr(item, 'end'):
            start = item.start
            end = item.end
        elif hasattr(item, 'time'):
            start = item.time
            end = item.time

        if not (end <= start_time or start >= end_time):
            if hasattr(item, 'start') and hasattr(item, 'end'):
                item.start = item.start - start_time
                item.end = item.end - start_time
            elif hasattr(item, 'time'):
                item.time = item.time - start_time

            filtered_elements.append(item)

    return filtered_elements


def split_score(score, split_every_sec):
    """Break the MIDI file into smaller parts."""

    end_time = score.get_end_time()

    # Get instruments
    instruments = score.instruments

    # Get all time signature changes
    time_signature_changes = score.time_signature_changes

    # Get all key changes
    key_changes = score.key_signature_changes

    print('Score with {} instruments, '
          '{} signature changes, '
          '{} key changes and duration of {} sec.'.format(
              len(instruments),
              len(time_signature_changes),
              len(key_changes),
              end_time))

    last_time_signature_change = None
    if len(time_signature_changes) > 0:
        last_time_signature_change = time_signature_changes[0]

    last_key_change = None
    if len(key_changes) > 0:
        last_key_change = key_changes[0]

    splits = []

    # Split score into smaller time spans
    for split_index, split_start_time in enumerate(range(0,
                                                         math.ceil(end_time),
                                                         split_every_sec)):
        split_end_time = min(split_start_time + split_every_sec, end_time)

        split_instruments = []
        split_notes_counter = 0

        print('Generate split #{} from {} sec - {} sec.'.format(
            split_index + 1, split_start_time, split_end_time))

        for instrument in instruments:
            # Find notes for this instrument in this range
            split_notes = find_elements_in_range(instrument.notes,
                                                 split_start_time,
                                                 split_end_time)

            split_notes_counter += len(split_notes)

            # Create new instrument
            split_instrument = pretty_midi.Instrument(program=instrument.program,
                                               name=instrument.name)

            split_instrument.notes = split_notes
            split_instruments.append(split_instrument)

        # Find key and time signature changes
        split_time_changes = find_elements_in_range(time_signature_changes,
                                                    split_start_time,
                                                    split_end_time)

        if len(split_time_changes) > 0:
            last_time_signature_change = split_time_changes[-1]
        elif last_time_signature_change:
            split_time_changes = [last_time_signature_change]

        split_key_signature_changes = find_elements_in_range(key_changes,
                                                             split_start_time,
                                                             split_end_time)

        if len(split_key_signature_changes) > 0:
            last_key_change = split_key_signature_changes[-1]
        elif last_key_change:
            split_key_signature_changes = [last_key_change]

        print('Found {} notes, '
              'added {} key changes and '
              '{} time signature changes.'.format(
                  split_notes_counter,
                  len(split_key_signature_changes),
                  len(split_time_changes)))

        splits.append({'instruments': split_instruments,
                       'time_signature_changes': split_time_changes,
                       'key_signature_changes': split_key_signature_changes})

    return splits


def generate_split_midi_files(target_folder, splits):
    """Saves multiple splitted MIDI files in a folder."""

    for split_index, split in enumerate(splits):
        split_score = pretty_midi.PrettyMIDI()
        split_score.time_signature_changes = split['time_signature_changes']
        split_score.key_signature_changes = split['key_signature_changes']
        split_score.instruments = split['instruments']

        # Return the split MIDI file
        # return split_score

        # Save MIDI file
        file_name = 'full_' + str(len(splits)) + '_' + 'split-{}'.format(split_index + 1) + '.mid'
        split_file_path = os.path.join(target_folder, file_name)
        split_score.write(split_file_path)

        print('Saved MIDI file at "{}".'.format(split_file_path))


def split_midi_file(infile, target_folder, split_every_sec):

    # Read MIDi file and clean up
    midi_data = pretty_midi.PrettyMIDI(infile)
    midi_data.remove_invalid_notes()

    # Split MIDI file!
    splits = split_score(midi_data, split_every_sec)

    # Generate MIDI files from splits
    generate_split_midi_files(target_folder, splits)


def split_midi_file_by_bins(infile, target_folder):

    midi_data = pretty_midi.PrettyMIDI(infile)
    total_time = math.ceil(midi_data.get_end_time())

    for split_every_sec in range(total_time):

        # [0, 1, 2] -> [1, 2, 3], if total time = 3
        split_every_sec = split_every_sec + 1

        split_midi_file(infile, target_folder, split_every_sec)


def plot_keyscape_from_midi(infile, source_folder):

    midi_data = pretty_midi.PrettyMIDI(infile)
    total_time = math.ceil(midi_data.get_end_time())

    bins = total_time
    bin_size_list = [total_time, 22, 15, 11, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    X = np.zeros((len(bin_size_list), bins))
    row = 0

    for bin_size in bin_size_list:

        num_of_segments = math.ceil(bins / bin_size)
        step = bin_size

        for segment_index in range(num_of_segments):

            print('Full %d -> split-%d' % (num_of_segments, segment_index+1))

            file_name = 'full_' + str(num_of_segments) + '_' + 'split-{}'.format(segment_index + 1) + '.mid'
            infile = os.path.join(source_folder, file_name)

            print('Input file:', infile)

            score = music21.converter.parse(infile)

            try:
                key = str(score.analyze('key'))
                print("Estimated key:", key)

                key_str = str(key).upper()
                print("Adjusted key:", key_str)

            except:
                key_str = 'NULL'

            key_cm_value = KEY_COLOR_DICT[key_str]
            print("Key color value:", key_cm_value)

            start_index = segment_index * step
            end_index = start_index + step

            print('Row: %d, Start array: %d, End array: %d' % (row, start_index, end_index))

            X[row, start_index:end_index] = key_cm_value
            # print(X[row])

        row = row + 1

    span = bins // len(bin_size_list)
    X_SPANNED = np.zeros((span * len(bin_size_list), bins))
    for row_ind, row in enumerate(X):
        for col in range(span):
            X_SPANNED[row_ind * span + col] = row

    # print("Original shape:", X.shape)
    # print("Expanded shape:", X_SPANNED.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(X_SPANNED, cmap=my_cmap, vmin=0, vmax=1)

    cbar = plt.colorbar(im)
    cbar.ax.get_yaxis().set_ticks([])
    for j, lab in enumerate(['     E Major', '     E Minor', '     D# Major', '     D# Minor', '     D Major',
                             '     D Minor', '     C# Major', '     C# Minor', '     C Major', '     C Minor',
                             '     B Major', '     B Minor', '     A# Major', '     A# Minor', '     A Major',
                             '     A Minor', '     G# Major', '     G# Minor', '     G Major', '     G Minor',
                             '     F# Major', '     F# Minor', '     F Major', '     F Minor', '     NULL']):
        cbar.ax.text(0., j/25, lab, ha='left', va='bottom')

    plt.show()
    fig.savefig('./pix/Chambermaid_Swing.png', dpi=fig.dpi)


if __name__ == '__main__':

    # Fugue No. 20 in A minor, BWV 865
    # Fugue No. 21 in B♭ major, BWV 866
    # fname = './data/fugue_a_minor_bwv865.wav'
    # fname = './data/looperman-swing-piano.wav'
    fname = './data/Chambermaid Swing - Parov Stelar.mp3'
    # fname = './data/full_104206.mid'

    # Use naive Bayes classifier to guess the key
    # estimate_key_by_naive_bayes(infile=fname)

    # Use Krumhansl-Schmuckler classifier to guess the key
    # estimate_key_by_krumhansl_schmuckler_classifier(infile=fname)

    # Plot the keyscape based on audio file
    plot_keyscape_from_audio(infile=fname)

    # Step 1: Split the midi file into segments
    # split_midi_file_by_bins(infile=fname, target_folder='swing')

    # Step 2: Plot the keyscape based on MIDI file
    # plot_keyscape_from_midi(infile=fname, source_folder='swing')
