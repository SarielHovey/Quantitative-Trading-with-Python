import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # Create a list of the number of coin tosses ("Bernoulli trials")
    number_of_trials = [0, 2, 10, 50, 200, 5000]

    data = stats.bernoulli.rvs(0.5, size=number_of_trials[-1])

    x = np.linspace(0, 1, 100)

    for i, N in enumerate(number_of_trials):
        # Accumulate the total number of heads for this # particular Bayesian update
        heads = data[:N].sum()
        ax = plt.subplot(len(number_of_trials) / 2, 2, i + 1)
        ax.set_title("%s trials, %s heads" % (N, heads))

        plt.xlabel("$P(H)$, Probability of Heads")
        plt.ylabel("Density")

        if i == 0:
            plt.ylim([0.0, 2.0])
        plt.setp(ax.get_yticklabels(), visible=False)

        # Create and plot a Beta distribution to represent the posterior belief in fairness of the coin.
        y = stats.beta.pdf(x, 1 + heads, 1 + N - heads)
        plt.plot(x, y, label="observe %d tosses,\n %d heads" % (N, heads))
        plt.fill_between(x, 0, y, color="#aaaadd", alpha=0.5)

    plt.tight_layout()
    plt.show()