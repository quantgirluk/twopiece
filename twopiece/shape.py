# -*- coding: utf-8 -*-
# name: twopiece.shape.py
# author: D.Santiago
# https://www.linkedin.com/in/dialidsantiago/
# @Quant_Girl
# --
# coding: utf-8


import scipy.stats

from twopiece.double import tpd_continuous
from twopiece.sinharcsinh import ssas
from twopiece.utils import display_dist


class TwoPieceShape(tpd_continuous):

    def __init__(self, f, loc=0.0, sigma=1.0, shape1=None, shape2=None):
        tpd_continuous.__init__(self, f, loc, sigma, sigma, None, None, shape1, shape2, 'boe')


class tpshastudent(TwoPieceShape):

    def __init__(self, loc=0.0, sigma=1.0, shape1=3.0, shape2=3.0):
        TwoPieceShape.__init__(self, scipy.stats.t, loc, sigma, shape1, shape2)


class tpshagennorm(TwoPieceShape):

    def __init__(self, loc=0.0, sigma=1.0, shape1=3.0, shape2=3.0):
        TwoPieceShape.__init__(self, scipy.stats.gennorm, loc, sigma, shape1, shape2)


class tpshasas(TwoPieceShape):

    def __init__(self, loc=0.0, sigma=None, shape1=3.0, shape2=3.0):
        TwoPieceShape.__init__(self, ssas, loc, sigma, shape1, shape2)


def display_tpshape(tpd='All', loc=0.0, sigma=1.0, shape1=2.0, shape2=6.0, show='random_sample', xlim=None):
    if tpd in ['All', 'student']:
        z = tpshastudent(loc=loc, sigma=sigma, shape1=shape1, shape2=shape2)
        display_dist(dist=z, color='dodgerblue', bound=True, name='dtpshstudent', show=show, xlim=xlim)

    if tpd in ['All', 'gennorm']:
        z = tpshagennorm(loc=loc, sigma=sigma, shape1=shape1, shape2=shape2)
        display_dist(dist=z, color='gold', name='tpshagennorm', show=show, xlim=xlim)

    if tpd in ['All', 'Sinhasinh']:
        z = tpshasas(loc=loc, sigma=sigma, shape1=shape1, shape2=shape2)
        display_dist(dist=z, color='deeppink', name='dtshapsas', show=show, xlim=xlim)

    return None

