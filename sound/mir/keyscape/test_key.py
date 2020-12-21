import numpy as np
import librosa
from matplotlib import cm
from matplotlib import pyplot as plt


NUM_NOTES = 12
NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
INTERVALS = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'd5', 'P5', 'm6', 'M6', 'm7', 'M7']
SCALES = ['major', 'minor']
# 'Typical' pitch distributions [A, A#, B, ..., G#] for major, minor scales with tonic A,
# adapted for use with other tonal centers by rotating.
MAJOR_SCALE_PROFILE = [0.16, 0.03, 0.09, 0.03, 0.13, 0.10, 0.06, 0.14, 0.03, 0.11, 0.03, 0.09]
MINOR_SCALE_PROFILE = [0.16, 0.03, 0.09, 0.13, 0.03, 0.10, 0.06, 0.14, 0.11, 0.03, 0.09, 0.03]

# Total number of colors to use
N = 7

# [0, 1] --> [purple, indigo, blue, green, yellow, orange, red]
color_map = cm.get_cmap('rainbow', N)

# [0. 0.16666667 0.33333333 0.5 0.66666667 0.83333333 1.]
Y = np.linspace(0, 1, N)

# Y[0] - Purple - A
# Y[1] - Indigo - D
# Y[2] - Blue - G
# Y[3] - Green - C
# Y[4] - Yellow - F
# Y[5] - Orange - B
# Y[6] - Red - E

# circle of fifths
KEY_COLOR_DICT = {
    'A': Y[0],
    'A#': Y[0],
    'B': Y[5],
    'C': Y[3],
    'C#': Y[3],
    'D': Y[1],
    'D#': Y[1],
    'E': Y[6],
    'F': Y[4],
    'F#': Y[4],
    'G': Y[2],
    'G#': Y[2]
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


if __name__ == '__main__':

    # Fugue No. 20 in A minor, BWV 865
    # Fugue No. 21 in B♭ major, BWV 866
    # fname = './data/fugue_a_minor_bwv865.wav'
    fname = './data/looperman-swing-piano.wav'

    # Use naive Bayes classifier to guess the key
    naive_bayes = NaiveBayes()
    dist = PitchDistribution.from_file(
        filename=fname,
        fraction=1.,
        seg_index=0)
    key_bayes = naive_bayes.get_key(dist)  # Returns Key object Key('G', 'major')
    print("Key in Bayes:", key_bayes)

    # Use Krumhansl-Schmuckler classifier to guess the key
    krumhansl_schmuckler = KrumhanslSchmuckler()
    dist = PitchDistribution.from_file(
        filename=fname,
        fraction=1.,
        seg_index=0)
    key_krumhansl = krumhansl_schmuckler.get_key(dist)  # Returns Key object Key('B', 'minor')
    print("Key in Krumhansl:", key_krumhansl)

    # Plot the keyscape
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

            dist = PitchDistribution.from_file(filename=fname, fraction=frac, seg_index=seg_index)
            key = krumhansl_schmuckler.get_key(dist)
            print("Estimated key:", key)

            key_str = str(key)
            key_str = key_str.split(" ")[0]
            key_cm_value = KEY_COLOR_DICT[key_str]
            print("Key color value:", key_cm_value)

            start_index = seg_index * step
            end_index = start_index + step

            print('Row:', row)
            print("Start array:", start_index)
            print('End array:', end_index)

            X[row, start_index:end_index] = key_cm_value
            print(X[row])

        row = row + 1

    span = bins // len(bin_size_list)
    X_SPANNED = np.zeros((span * len(bin_size_list), bins))
    for row_ind, row in enumerate(X):
        for col in range(span):
            X_SPANNED[row_ind * span + col] = row

    print("Original shape:", X.shape)
    print("Expanded shape:", X_SPANNED.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(X_SPANNED, cmap=color_map, vmin=0, vmax=1)
    plt.colorbar(im)
    plt.show()
    fig.savefig('./pix/swing.png', dpi=fig.dpi)



