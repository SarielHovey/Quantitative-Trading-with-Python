import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymc3 as pm
# Refer to pymc3 document is suggested since it's very user-friendly.
# https://docs.pymc.io/notebooks/GLM-linear.html
sns.set(style="darkgrid", palette="muted")
plt.style.use("seaborn")

def simulate_linear_data(N, beta_0, beta_1, eps_sigma_sq):
    """
    Simulate a random dataset using a noisy linear process.

    N: Number of data points to simulate
    beta_0: Intercept
    beta_1: Slope of univariate predictor, X
    """
    # Create a pandas DataFrame with column 'x' containing N uniformly sampled values between 0.0 and 1.0
    df = pd.DataFrame(
        {"x":
            np.random.choice(
                np.arange(100)/100.0, N, replace=True
            )
        }
    )
    # Use a linear model (y ~ beta_0 + beta_1*x + epsilon) to generate a column 'y' of responses based on 'x'
    eps_mean = 0.0
    df["y"] = beta_0 + beta_1*df["x"] + np.random.normal(eps_mean, eps_sigma_sq, N)
    return df

def glm_mcmc_inference(df, iterations=5000):
    """
    Calculates the Markov Chain Monte Carlo trace of a Generalised Linear Model Bayesian linear regression model on supplied data.

    df: DataFrame containing the data
    iterations: Number of iterations to carry out MCMC for
    """
    basic_model = pm.Model()
    with basic_model:
        # Create the glm using the Patsy model syntax
        # We use a Normal distribution for the likelihood
        pm.glm.GLM.from_formula("y ~ x", df, family=pm.glm.families.Normal())
        # Use Maximum A Posteriori (MAP) optimisation
        start = pm.find_MAP()
        # Use the No-U-Turn Sampler
        step = pm.NUTS()
        # Calculate the trace
        trace = pm.sample(iterations, step, start, progressbar=True, cores=12)

    return trace

if __name__ == "__main__":
    # These are our "true" parameters
    beta_0 = 1.0 # Intercept
    beta_1 = 2.0 # Slope

    # Simulate 100 data points, with a variance of 0.5
    N = 100
    eps_sigma_sq = 0.5

    # Simulate the "linear" data using the above parameters
    df = simulate_linear_data(N, beta_0, beta_1, eps_sigma_sq)

    # Plot the data, and a frequentist linear regression fit
    sns.lmplot(x="x", y="y", data=df, size=10)
    plt.xlim(0.0, 1.0)
    
    trace = glm_mcmc_inference(df, iterations=5000)
    pm.traceplot(trace[500:])
    plt.show()
    plt.savefig('1.png')
    plt.clf()

    # Plot a sample of posterior regression lines
    sns.lmplot(x="x", y="y", data=df, size=10, fit_reg=False) # Dont plot frequencist regression line
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 4.0)
    pm.plot_posterior_predictive_glm(trace, samples=100)
    x = np.linspace(0, 1, N)
    y = beta_0 + beta_1*x
    plt.plot(x, y, label="True Regression Line", lw=3., c="green")
    plt.legend(loc=0)
    plt.show()
    plt.savefig('2.png')