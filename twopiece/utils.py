import math

import matplotlib.pyplot as plt
from numpy import min, max, arange
from seaborn import distplot
from seaborn import set

set(style='whitegrid', rc={"grid.linewidth": 0.75, "figure.figsize": (9, 6)})


def get_sigma1_sigma2(sigma, gamma, kind):
    """
    Gets the scale parameters sigma1, sigma2 from sigma and gamma

    :param sigma: scale parameter
    :param gamma: skewness or asymmetry parameter
    :param kind: Parametrisation name
    :return:
    """

    if kind == 'inverse_scale':

        if gamma < 0:
            raise AssertionError("Gamma parameter must be positive")
        sigma1 = sigma / gamma
        sigma2 = sigma * gamma

    elif kind == 'epsilon_skew':

        if gamma >= 1 or gamma <= -1:
            raise AssertionError("Gamma parameter must be positive")

        sigma1 = sigma * (1 + gamma)
        sigma2 = sigma * (1 - gamma)

    elif kind == 'percentile':

        if gamma >= 1 or gamma <= 0:
            raise AssertionError("Gamma parameter must be in (0,1)")

        sigma1 = sigma * gamma
        sigma2 = sigma * (1 - gamma)

    else:
        if gamma >= 1 or gamma <= -1:
            raise AssertionError("Skewness parameters must be in (-1, 1).")

        sigma1 = sigma / math.sqrt(1 + gamma)
        sigma2 = sigma / math.sqrt(1 - gamma)

    return sigma1, sigma2


def display_dist(dist, name='', color='dodgerblue', bound=False, show='random_sample', xlim=None):
    """
    Shows graphs for a given two piece distribution
    :param dist: distribution instance
    :param name: string, name
    :param color: string, color
    :param bound: boolean, bounding the x axis for better display
    :param show: string, All, pdf, cds, ppf, sample
    :param xlim: overwrites the xlim for the plots
    :return: 1
    """

    if show in ['All', 'pdf']:

        x = arange(-10, 10, 0.01)
        y = dist.pdf(x)
        plt.figure('Probability Density Function')
        plt.plot(x, y, marker='', linestyle='solid', color=color)
        if xlim:
            plt.xlim(xlim)
        plt.title(name + ' pdf')
        plt.show()

    if show in ['All', 'cdf']:
        x = arange(-10, 10, 0.01)
        y = dist.cdf(x)
        plt.figure('Cumulative Distribution Function')
        plt.plot(x, y, marker='', linestyle='solid', color=color)
        if xlim:
            plt.xlim(xlim)
        plt.title(name + ' cdf')
        plt.show()

    if show in ['All', 'ppf']:
        x = arange(0.001, 0.999, 0.001)
        y = dist.ppf(x)
        plt.figure('Quantile Function')
        plt.plot(x, y, marker='', linestyle='solid', color=color)
        plt.title(name + ' ppf')
        plt.show()

    if show in ['All', 'random_sample']:

        sample = dist.random_sample(1000)

        if bound:
            sample = sample[abs(sample) < 25]

        plt.figure('Random Sample')
        distplot(sample, bins=50, kde=False, norm_hist=True,
                 hist_kws=dict(edgecolor="white", color=color, linewidth=1.0, alpha=0.60))
        x = arange(min(sample) - 2, max(sample) + 2, 0.01)
        y = dist.pdf(x)
        plt.plot(x, y, marker='', linestyle='solid', color=color)
        if xlim:
            plt.xlim(xlim)
        plt.title(name + ' random sample')
        plt.show()

    return None


def display_parameterisations(dist=None, loc=0.0, sigma1=1.0, sigma2=1.0, sigma=1.0, gamma=0.5, show='random_sample'):
    z = dist(loc=loc, sigma1=sigma1, sigma2=sigma2)
    display_dist(dist=z, color='blue', name='standard', show=show)

    z = dist(loc=loc, sigma=sigma, gamma=gamma, kind='boe')
    display_dist(dist=z, color='coral', name='boe', show=show)

    z = dist(loc=loc, sigma=sigma, gamma=gamma, kind='inverse_scale')
    display_dist(dist=z, color='red', name='inverse_scale', show=show)

    z = dist(loc=loc, sigma=sigma, gamma=gamma, kind='percentile')
    display_dist(dist=z, color='black', name='percentile', show=show)

    return None


def display_parameterisations_shape(dist=None, loc=0.0, sigma1=1.0, sigma2=1.0,
                                    sigma=1.0, gamma=0.5, shape=2.0, show='random_sample'):
    z = dist(loc=loc, sigma1=sigma1, sigma2=sigma2, shape=shape)
    display_dist(dist=z, color='dodgerblue', name='standard', show=show)

    z = dist(loc=loc, sigma=sigma, gamma=gamma, shape=shape, kind='boe')
    display_dist(dist=z, color='coral', name='boe', show=show)

    z = dist(loc=loc, sigma=sigma, gamma=gamma, shape=shape, kind='inverse_scale')
    display_dist(dist=z, color='red', name='inverse_scale', show=show)

    z = dist(loc=loc, sigma=sigma, gamma=gamma, shape=shape, kind='percentile')
    display_dist(dist=z, color='black', name='percentile', show=show)

    return None
