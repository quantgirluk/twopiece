# -*- coding: utf-8 -*-
# name: twopiece.scale.py
# author: D.Santiago
# https://www.linkedin.com/in/dialidsantiago/
# @Quant_Girl
# --
# coding: utf-8

import math

import numpy as np
import scipy.stats
from numpy import isscalar, asarray, random, sum, empty

from twopiece.sinharcsinh import ssas
from twopiece.utils import display_dist


def pdf_tp_generic(x, pdf, loc, sigma1, sigma2):
    """
    Probability density function at x of the defined two piece distribution.

    :param x: array like
    :param pdf: a probability density function from a symmetric distribution defined on R.
    :param loc: location parameter
    :param sigma1: shape parameter
    :param sigma2: shape parameter
    :return: pdf of the defined two piece in x

    """

    if sigma1 * sigma2 <= 0:
        raise AssertionError('Scale parameters must be positive.')

    aux = 2 / (sigma1 + sigma2)

    if isscalar(x):

        if x < loc:

            output = aux * pdf((x - loc) / sigma1)

        else:

            output = aux * pdf((x - loc) / sigma2)
    else:

        x = asarray(x)
        output = empty(x.size)
        index = x < loc
        output[index] = aux * pdf((x[index] - loc) / sigma1)
        index = x >= loc
        output[index] = aux * pdf((x[index] - loc) / sigma2)

    return output


def cdf_tp_generic(x, cdf, loc, sigma1, sigma2):
    """
    Cumulative Density Function at x of the defined two piece distribution.

    :param x: array like
    :param cdf: a cumulative density function from a symmetric distribution defined on R.
    :param loc: location parameter
    :param sigma1: scale parameter
    :param sigma2: scale parameter
    :return:

    """

    if sigma1 * sigma2 <= 0:
        raise AssertionError('Scale parameters must be positive.')

    aux = 2 / (sigma1 + sigma2)

    if isscalar(x):

        if x < loc:
            output = aux * sigma1 * cdf((x - loc) / sigma1)
        else:
            output = 1 - aux * sigma2 * (1 - cdf((x - loc) / sigma2))

    else:
        x = asarray(x)
        output = empty(x.size)
        index = x < loc
        output[index] = aux * sigma1 * cdf((x[index] - loc) / sigma1)
        index = x >= loc
        output[index] = 1 - aux * sigma2 * (1 - cdf((x[index] - loc) / sigma2))

    return output


def qqf_tp_generic(q, qqf, loc, sigma1, sigma2):
    """
    Quantile Function at q of the defined two piece distribution.

    :param q: array like
    :param qqf: a quantile function (ppf) from a symmetric distribution defined on R.
    :param loc: location parameter
    :param sigma1: scale parameter
    :param sigma2: scale parameter
    :return:
    """

    if sigma1 * sigma2 <= 0:
        raise AssertionError('Scale parameters must be positive.')

    p = sigma1 / (sigma1 + sigma2)

    if isscalar(q):

        if q > 1 or q < 0:
            raise AssertionError('Quantile Function is defined on (0,1).')

        if q <= p:

            output = loc + sigma1 * qqf(0.5 * (sigma1 + sigma2) * q / sigma1)

        else:
            output = loc + sigma2 * qqf(0.5 * ((sigma1 + sigma2) * (1 + q) - 2 * sigma1) / sigma2)

    else:

        q = asarray(q)

        if sum((q > 1) | (q < 0)) > 0:
            raise AssertionError('Quantile Function is defined on (0,1).')

        output = empty(q.size)
        index = q <= p
        output[index] = loc + sigma1 * qqf(0.5 * (sigma1 + sigma2) * q[index] / sigma1)
        index = q > p
        output[index] = loc + sigma2 * qqf(0.5 * ((sigma1 + sigma2) * (1 + q[index]) - 2 * sigma1) / sigma2)

    return output


def random_tp_sample(size, qqf, loc, sigma1, sigma2):
    """
    Random Sample Generation

    :param size: integer, sample size
    :param qqf: a quantile function (ppf) from a symmetric distribution defined on R
    :param loc: location parameter
    :param sigma1: scale parameter
    :param sigma2: scale parameter
    :return:
    """
    if not isinstance(size, int):
        raise TypeError('Sample size must be integer.')

    if sigma1 * sigma2 <= 0:
        raise AssertionError('Scale parameters must be positive.')

    alpha = random.rand(size)
    p = sigma1 / (sigma1 + sigma2)

    if isscalar(alpha):

        if alpha <= p:

            qq = loc + sigma1 * qqf(0.5 * (sigma1 + sigma2) * alpha / sigma1)

        else:
            qq = loc + sigma2 * qqf(0.5 * ((sigma1 + sigma2) * (1 + alpha) - 2 * sigma1) / sigma2)

    else:

        alpha = asarray(alpha)
        qq = empty(alpha.size)
        index = alpha <= p
        qq[index] = loc + sigma1 * qqf(0.5 * (sigma1 + sigma2) * alpha[index] / sigma1)
        index = alpha > p
        qq[index] = loc + sigma2 * qqf(0.5 * ((sigma1 + sigma2) * (1 + alpha[index]) - 2 * sigma1) / sigma2)

    return qq


def get_sigma1_sigma2(sigma, gamma, kind):
    """
    Gets the scale parameters sigma1, sigma2 from sigma and gamma
    :param sigma: scale parameter
    :param gamma: skewness or asymmetry parameter
    :param kind: Parametrisation name
    :return: sigma1 and sigma2 scale parameters
    """

    if kind == 'inverse_scale':

        if gamma <= 0:
            raise AssertionError("Gamma parameter must be positive")
        sigma1 = sigma / gamma
        sigma2 = sigma * gamma

    elif kind == 'epsilon_skew':

        if gamma >= 1 or gamma <= -1:
            raise AssertionError("Gamma parameter must be in (-1, 1)")

        sigma1 = sigma * (1 + gamma)
        sigma2 = sigma * (1 - gamma)

    elif kind == 'percentile':

        if gamma >= 1 or gamma <= 0:
            raise AssertionError("Gamma parameter must be in (0,1)")

        sigma1 = sigma * gamma
        sigma2 = sigma * (1 - gamma)

    elif kind == 'boe':

        if gamma == 0:
            actual_gamma = 0
        else:
            s = gamma / sigma
            actual_gamma_unsigned = np.sqrt(1 - 4 * ((np.sqrt(1 + np.pi * s ** 2) - 1) / (np.pi * s ** 2)) ** 2)
            actual_gamma = actual_gamma_unsigned if gamma > 0 else -actual_gamma_unsigned

        sigma1 = sigma / math.sqrt(1 + actual_gamma)
        sigma2 = sigma / math.sqrt(1 - actual_gamma)

    else:
        raise ValueError('Invalid Parametrisation')

    return sigma1, sigma2


class TwoPiece:

    def __init__(self, f, loc, sigma1, sigma2, sigma, gamma, kind):

        """

        :param f: continuous symmetric distribution with support on R
        :param loc: location parameter
        :param sigma1: scale parameter
        :param sigma2: scale parameter
        :param sigma: scale parameter
        :param gamma: skewness or asymmetry parameter
        :param kind: Parametrisation
        """

        if all(v is None for v in {sigma1, sigma2, sigma, gamma, kind}):
            raise AssertionError('Expected either (sigma1, sigma2) or (sigma, gamma, kind).')

        if kind:
            if kind not in {'inverse_scale', 'epsilon_skew', 'percentile', 'boe'}:
                raise AssertionError('Invalid Parametrisation')

        self.f = f
        self.loc = loc
        self.sigma = sigma
        self.gamma = gamma
        self.kind = kind

        if sigma1 and sigma2:

            self.sigma1 = sigma1
            self.sigma2 = sigma2

        else:

            try:
                sigma1, sigma2 = get_sigma1_sigma2(self.sigma, self.gamma, self.kind)
                self.sigma1 = sigma1
                self.sigma2 = sigma2

            except BaseException:
                print('Missing or Invalid Arguments')


class TwoPieceScale(TwoPiece):

    def pdf(self, x):
        s = pdf_tp_generic(x, self.f.pdf, self.loc, self.sigma1, self.sigma2)
        return s

    def cdf(self, x):
        s = cdf_tp_generic(x, self.f.cdf, self.loc, self.sigma1, self.sigma2)

        return s

    def ppf(self, x):
        qq = qqf_tp_generic(x, self.f.ppf, self.loc, self.sigma1, self.sigma2)

        return qq

    def random_sample(self, size):
        sample = random_tp_sample(size, self.f.ppf, self.loc, self.sigma1, self.sigma2)

        return sample


class tpnorm(TwoPieceScale):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, kind=None):
        TwoPieceScale.__init__(self, scipy.stats.norm, loc, sigma1, sigma2, sigma, gamma, kind)


class tplaplace(TwoPieceScale):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, kind=None):
        TwoPieceScale.__init__(self, scipy.stats.laplace, loc, sigma1, sigma2, sigma, gamma, kind)


class tpcauchy(TwoPieceScale):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, kind=None):
        TwoPieceScale.__init__(self, scipy.stats.cauchy, loc, sigma1, sigma2, sigma, gamma, kind)


class tplogistic(TwoPieceScale):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, kind=None):
        TwoPieceScale.__init__(self, scipy.stats.logistic, loc, sigma1, sigma2, sigma, gamma, kind)


class TwoPieceScalewithShape:

    def __init__(self, f, loc, sigma1, sigma2, sigma, gamma, shape, kind):

        if all(v is None for v in {sigma1, sigma2, sigma, gamma}):
            raise ValueError('Expected either (sigma1, sigma2) or (sigma, gamma).')

        if kind not in {'inverse_scale', 'epsilon_skew', 'percentile', 'boe'}:
            raise ValueError('Invalid Parametrisation. Choose one of the following: inverse_scale, epsilon_skew, '
                             'percentile, boe')

        self.loc = loc
        self.sigma = sigma
        self.gamma = gamma
        self.f = f(shape)
        self.kind = kind

        if sigma1 and sigma2:

            self.sigma1 = sigma1
            self.sigma2 = sigma2

        else:

            try:

                sigma1, sigma2 = get_sigma1_sigma2(self.sigma, self.gamma, self.kind)
                self.sigma1 = sigma1
                self.sigma2 = sigma2

            except Exception:
                print('Exception Missing or Invalid Arguments')


class tp_scalesh(TwoPieceScalewithShape):

    def pdf(self, x):
        s = pdf_tp_generic(x, self.f.pdf, self.loc, self.sigma1, self.sigma2)
        return s

    def cdf(self, x):
        s = cdf_tp_generic(x, self.f.cdf, self.loc, self.sigma1, self.sigma2)
        return s

    def ppf(self, x):
        qq = qqf_tp_generic(x, self.f.ppf, self.loc, self.sigma1, self.sigma2)
        return qq

    def random_sample(self, size):
        sample = random_tp_sample(size, self.f.ppf, self.loc, self.sigma1, self.sigma2)
        return sample


class tpstudent(tp_scalesh):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, shape=None, kind=None):
        tp_scalesh.__init__(self, scipy.stats.t, loc, sigma1, sigma2, sigma, gamma, shape, kind)


class tpgennorm(tp_scalesh):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, shape=None, kind=None):
        tp_scalesh.__init__(self, scipy.stats.gennorm, loc, sigma1, sigma2, sigma, gamma, shape, kind)


class tpsas(tp_scalesh):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, shape=None, kind=None):
        tp_scalesh.__init__(self, ssas, loc, sigma1, sigma2, sigma, gamma, shape, kind)


def display_tpscale(tpdist='All', loc=0.0, sigma1=1.0, sigma2=1.0, shape=3.0, show='random_sample'):
    if tpdist in ['All', 'tpnorm']:
        z = tpnorm(loc=loc, sigma1=sigma1, sigma2=sigma2)
        display_dist(dist=z, color='dodgerblue', name='tpnorm', show=show)

    if tpdist in ['All', 'tplaplace']:
        z = tplaplace(loc=loc, sigma1=sigma1, sigma2=sigma2)
        display_dist(dist=z, color='greenyellow', name='tplaplace', show=show)

    if tpdist in ['All', 'tpcauchy']:
        z = tpcauchy(loc=loc, sigma1=sigma1, sigma2=sigma2)
        display_dist(dist=z, color='orange', bound=True, name='tpcauchy', show=show)

    if tpdist in ['All', 'tplogistic']:
        z = tplogistic(loc=loc, sigma1=sigma1, sigma2=sigma2)
        display_dist(dist=z, color='aquamarine', name='tplogistic', show=show)

    if tpdist in ['All', 'tpstudent']:
        z = tpstudent(loc=loc, sigma1=sigma1, sigma2=sigma2, shape=shape)
        display_dist(dist=z, color='gold', name='tpstudent', show=show)

    if tpdist in ['All', 'tpgennorm']:
        z = tpgennorm(loc=loc, sigma1=sigma1, sigma2=sigma2, shape=shape)
        display_dist(dist=z, color='cyan', name='tpgen_norm', show=show)

    if tpdist in ['All', 'tpsas']:
        z = tpsas(loc=loc, sigma1=sigma1, sigma2=sigma2, shape=shape)
        display_dist(dist=z, color='deeppink', name='tpsas', show=show)

    return None
