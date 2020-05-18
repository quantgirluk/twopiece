from math import asinh, cosh, sqrt, sinh

import scipy.stats
from numpy import random, vectorize


def _pdf_instance(x, pdf, loc, scale, delta, epsilon):
    z = (x - loc) / scale
    output = (delta / scale) * pdf(sinh(delta * asinh(z) - epsilon)) * cosh(delta * asinh(z) - epsilon) / sqrt(
        1 + z * z)
    return output


def _cdf_instance(x, cdf, loc, scale, delta, epsilon):
    z = (x - loc) / scale
    output = cdf(sinh(delta * asinh(z) - epsilon))

    return output


def _qqf_instance(q, qqf, loc, scale, delta, epsilon):
    output = loc + scale * sinh((asinh(qqf(q)) + epsilon) / delta)
    return output


def _random_sample(size, qqf, loc, scale, delta, epsilon):
    alpha = random.rand(size)
    qqfv = vectorize(_qqf_instance)

    return qqfv(alpha, qqf, loc, scale, delta, epsilon)


class SinhArcsinh:

    def __init__(self, f, loc, scale, delta, epsilon):
        self.f = f
        self.loc = loc
        self.scale = scale
        self.delta = delta
        self.epsilon = epsilon

    def pdf(self, x):
        _pdf_vector = vectorize(_pdf_instance)
        s = _pdf_vector(x, self.f.pdf, self.loc, self.scale, self.delta, self.epsilon)
        return s

    def cdf(self, x):
        _cdf_vector = vectorize(_cdf_instance)
        s = _cdf_vector(x, self.f.cdf, self.loc, self.scale, self.delta, self.epsilon)
        return s

    def ppf(self, q):
        _qqf_vector = vectorize(_qqf_instance)
        x = _qqf_vector(q, self.f.ppf, self.loc, self.scale, self.delta, self.epsilon)

        return x

    def random_sample(self, size):
        sample = _random_sample(size, self.f.ppf, self.loc, self.scale, self.delta, self.epsilon)
        return sample


class sinhasinh(SinhArcsinh):

    def __init__(self, loc=0.0, scale=1.0, delta=1.0, epsilon=0.0):
        SinhArcsinh.__init__(self, scipy.stats.norm, loc, scale, delta, epsilon)


class ssas(SinhArcsinh):

    def __init__(self, delta=1.0):
        SinhArcsinh.__init__(self, f=scipy.stats.norm, loc=0.0, scale=1.0, delta=delta, epsilon=0.0)
