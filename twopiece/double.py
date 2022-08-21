# -*- coding: utf-8 -*-
# name: twopiece.double.py
# author: D.Santiago
# https://www.linkedin.com/in/dialidsantiago/
# @Quant_Girl
# --
# coding: utf-8


import scipy.stats
from numpy import isscalar, asarray, random, sum, empty

from twopiece.sinharcsinh import ssas
from twopiece.utils import get_sigma1_sigma2, display_dist


def pdf_tpd_generic(x, pdf1, pdf2, loc, sigma1, sigma2, epsilon):
    """
    Probability density function at x of the defined two piece distribution.
    :param x: array like
    :param pdf1:
    :param pdf2:
    :param loc: location parameter
    :param sigma1: scale parameter
    :param sigma2: scale parameter
    :param epsilon: shape parameter
    :return: pdf of the defined two piece in x

    """

    if sigma1 * sigma2 <= 0:
        raise ValueError('Scale parameters must be positive.')

    aux1 = 2 * epsilon / sigma1
    aux2 = 2 * (1 - epsilon) / sigma2

    if isscalar(x):
        if x < loc:
            output = aux1 * pdf1((x - loc) / sigma1)
        else:
            output = aux2 * pdf2((x - loc) / sigma2)
    else:
        x = asarray(x)
        output = empty(x.size)
        index = x < loc
        output[index] = aux1 * pdf1((x[index] - loc) / sigma1)
        index = x >= loc
        output[index] = aux2 * pdf2((x[index] - loc) / sigma2)

    return output


def cdf_tpd_generic(x, cdf1, cdf2, loc, sigma1, sigma2, epsilon):
    """
    Cumulative Density Function at x of the defined two piece distribution.

    :param x: array like
    :param cdf1: a cumulative density function from a symmetric distribution defined on R.
    :param cdf2: a cumulative density function from a symmetric distribution defined on R.
    :param loc: location parameter
    :param sigma1: scale parameter
    :param sigma2: scale parameter
    :param epsilon: shape parameter
    :return:

    """

    if sigma1 * sigma2 <= 0:
        raise ValueError('Scale parameters must be positive.')
    if isscalar(x):
        if x < loc:
            output = 2 * epsilon * cdf1((x - loc) / sigma1)
        else:
            output = epsilon + (1 - epsilon) * (2 * cdf2((x - loc) / sigma2) - 1)
    else:
        x = asarray(x)
        output = empty(x.size)
        index = x < loc
        output[index] = 2 * epsilon * cdf1((x[index] - loc) / sigma1)
        index = x >= loc
        output[index] = epsilon + (1 - epsilon) * (2 * cdf2((x[index] - loc) / sigma2) - 1)

    return output


def qqf_tpd_generic(q, qqf1, qqf2, loc, sigma1, sigma2, epsilon):
    """
    Quantile Function at q of the defined two piece distribution.

    :param q: array like
    :param qqf1: a quantile function (ppf) from a symmetric distribution defined on R.
    :param qqf2: a quantile function (ppf) from a symmetric distribution defined on R.
    :param loc: location parameter
    :param sigma1: scale parameter
    :param sigma2: scale parameter
    :param epsilon: shape parameter
    :return:
    """

    if sigma1 * sigma2 <= 0:
        raise ValueError('Scale parameters must be positive.')

    if isscalar(q):
        if q > 1 or q < 0:
            raise ValueError('Quantile Function is defined on (0,1).')
        if q <= epsilon:
            output = loc + sigma1 * qqf1((0.5 / epsilon) * q)
        else:
            aux = 0.5 * ((q - epsilon) / (1 - epsilon) + 1)
            output = loc + sigma2 * qqf2(aux)
    else:
        q = asarray(q)
        if sum((q > 1) | (q < 0)) > 0:
            raise ValueError('Quantile Function is defined on (0,1).')
        output = empty(q.size)
        index = q <= epsilon
        output[index] = loc + sigma1 * qqf1((0.5 / epsilon) * q[index])
        index = q > epsilon
        aux = 0.5 * ((q[index] - epsilon) / (1 - epsilon) + 1)
        output[index] = loc + sigma2 * qqf2(aux)

    return output


def random_tpd_sample(size, qqf1, qqf2, loc, sigma1, sigma2, epsilon):
    """
    Random Sample Generation

    :param size: integer, sample size
    :param qqf1: a quantile function (qqf) from a symmetric distribution defined on R.
    :param qqf2: a quantile function (qqf) from a symmetric distribution defined on R.
    :param loc: location parameter
    :param sigma1: scale parameter
    :param sigma2: scale parameter
    :param epsilon: shape parameter
    :return:
    """
    if not isinstance(size, int):
        raise TypeError('Sample size must be of type integer.')

    if sigma1 * sigma2 <= 0:
        raise ValueError('Scale parameters must be positive.')

    alpha = random.rand(size)

    if isscalar(alpha):
        if alpha <= epsilon:
            qq = loc + sigma1 * qqf1(0.5 * alpha / epsilon)
        else:
            qq = loc + sigma2 * qqf2(0.5 * ((alpha - epsilon) / (1 - epsilon) + 1))
    else:
        alpha = asarray(alpha)
        qq = empty(alpha.size)
        index = alpha <= epsilon
        qq[index] = loc + sigma1 * qqf1(0.5 * alpha[index] * (1 / epsilon))
        index = alpha > epsilon
        qq[index] = loc + sigma2 * qqf2(0.5 * ((alpha[index] - epsilon) / (1 - epsilon) + 1))

    return qq


class TwoPieceDouble:

    def __init__(self, f, loc, sigma1, sigma2, sigma, gamma, shape1, shape2, kind):

        """

        :param f: continuous symmetric distribution with support on R
        :param loc: location parameter
        :param sigma1: scale parameter
        :param sigma2: scale parameter
        :param sigma: scale parameter
        :param gamma: skewness or asymmetry parameter
        :param shape1: shape parameter
        :param shape2: shape parameter
        :param kind: Parametrisation
        """

        if all(v is None for v in {sigma1, sigma2, sigma, gamma, kind}):
            raise AssertionError('Expected either (sigma1, sigma2) or (sigma, gamma, kind).')

        if kind:
            if kind not in {'inverse_scale', 'epsilon_skew', 'percentile', 'boe'}:
                raise ValueError('Invalid value of kind provided. Valid values are boe, '
                                 'inverse_scale, epsilon_skew, percentile.')

        self.f = f
        self.loc = loc
        self.sigma = sigma
        self.gamma = gamma
        self.shape1 = shape1
        self.shape2 = shape2
        self.kind = kind

        if sigma1 and sigma2:
            self.sigma1 = sigma1
            self.sigma2 = sigma2
        else:
            sigma1, sigma2 = get_sigma1_sigma2(self.sigma, self.gamma, self.kind)
            self.sigma1 = sigma1
            self.sigma2 = sigma2


class tpd_continuous(TwoPieceDouble):

    def __init__(self, f, loc, sigma1, sigma2, sigma, gamma, shape1, shape2, kind):
        super().__init__(f, loc, sigma1, sigma2, sigma, gamma, shape1, shape2, kind)

        self.f1 = self.f(self.shape1)
        self.f2 = self.f(self.shape2)
        self.epsilon = self.sigma1 * self.f2.pdf(0) / (self.sigma1 * self.f2.pdf(0) + self.sigma2 * self.f1.pdf(0))

    def pdf(self, x):
        s = pdf_tpd_generic(x, self.f1.pdf, self.f2.pdf, self.loc, self.sigma1, self.sigma2, self.epsilon)
        return s

    def cdf(self, x):
        s = cdf_tpd_generic(x, self.f1.cdf, self.f2.cdf, self.loc, self.sigma1, self.sigma2, self.epsilon)
        return s

    def ppf(self, x):
        qq = qqf_tpd_generic(x, self.f1.ppf, self.f2.ppf, self.loc, self.sigma1, self.sigma2, self.epsilon)
        return qq

    def random_sample(self, size):
        sample = random_tpd_sample(size, self.f1.ppf, self.f2.ppf, self.loc, self.sigma1, self.sigma2, self.epsilon)
        return sample


class dtpstudent(tpd_continuous):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, shape1=None, shape2=None, kind=None):
        tpd_continuous.__init__(self, scipy.stats.t, loc, sigma1, sigma2, sigma, gamma, shape1, shape2, kind)


class dtpgennorm(tpd_continuous):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, shape1=None, shape2=None, kind=None):
        tpd_continuous.__init__(self, scipy.stats.gennorm, loc, sigma1, sigma2, sigma, gamma, shape1, shape2, kind)


class dtpsas(tpd_continuous):

    def __init__(self, loc=0.0, sigma1=None, sigma2=None, sigma=None, gamma=None, shape1=None, shape2=None, kind=None):
        tpd_continuous.__init__(self, ssas, loc, sigma1, sigma2, sigma, gamma, shape1, shape2, kind)


def display_dtp(tpd='All', loc=0.0, sigma1=1.0, sigma2=0.5, shape1=2.0, shape2=6.0, show='random_sample', xlim=None):
    if tpd in ['All', 'dtpstudent']:
        z = dtpstudent(loc=loc, sigma1=sigma1, sigma2=sigma2, shape1=shape1, shape2=shape2)
        display_dist(dist=z, color='dodgerblue', bound=True, name='dtpstudent', show=show, xlim=xlim)

    if tpd in ['All', 'dtpgennorm']:
        z = dtpgennorm(loc=loc, sigma1=sigma1, sigma2=sigma2, shape1=shape1, shape2=shape2)
        display_dist(dist=z, color='gold', name='dtpgennorm', show=show, xlim=xlim)

    if tpd in ['All', 'dtpsas']:
        z = dtpsas(loc=loc, sigma1=sigma1, sigma2=sigma2, shape1=shape1, shape2=shape2)
        display_dist(dist=z, color='deeppink', name='dtpsas', show=show, xlim=xlim)

    return None
