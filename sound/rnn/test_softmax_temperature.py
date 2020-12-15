import numpy as np
from matplotlib import pyplot as plt

def reweight_distribution(original_distribution, temperature=0.5):
    """Reweight a probability distribution to increase or decrease entropy.

    # Arguments
        original_distribution: A 1D Numpy array of probability values.
            Must sum to one.
        temperature: Factor quantifying the entropy of the output distribution.

    # Returns
        A re-weighted version of the original distribution.
    """
    distribution = np.log(original_distribution) / temperature
    distribution = np.exp(distribution)
    # The sum of the distribution may no longer be 1!
    # Thus we divide it by its sum to obtain the new distribution.
    return distribution / np.sum(distribution)

def plot_hist(original_distribution):

    temp_001 = reweight_distribution(original_distribution, 0.01)
    temp_020 = reweight_distribution(original_distribution, 0.20)
    temp_040 = reweight_distribution(original_distribution, 0.40)
    temp_060 = reweight_distribution(original_distribution, 0.60)
    temp_080 = reweight_distribution(original_distribution, 0.80)
    temp_100 = reweight_distribution(original_distribution, 1.00)

    plt.hist([temp_001, temp_020, temp_040, temp_060, temp_080, temp_100],
             bins=10,
             alpha=0.5,
             label=['temp_001', 'temp_020', 'temp_040', 'temp_060', 'temp_080', 'temp_100'])

    plt.legend(loc='upper right')

    plt.show()


if __name__ == '__main__':

    dist = np.random.normal(0.5, 0.1, 10)
    dist = dist / np.sum(dist)

    plot_hist(dist)