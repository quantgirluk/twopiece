import unittest
from twopiece.scale import tpnorm, get_sigma1_sigma2
import numpy as np
from parameterized import parameterized


class TestTwoPiece(unittest.TestCase):

    @parameterized.expand([
                          [0.0, 1.0, 0.0],
                          [0.0, 1.0, 1.0], [0.0, 1.0, -1.0],
                          [0.0, 1.0, 2.0], [0.0, 1.0, -2.0], ])
    def test_boe_parametrisation(self, mu, sigma, gamma):

        sigma1, sigma2 = get_sigma1_sigma2(sigma, gamma, kind='boe')
        dist = tpnorm(mu, sigma1=sigma1, sigma2=sigma2)
        dist_boe = tpnorm(loc=mu, sigma=sigma, gamma=gamma, kind='boe')

        x = np.arange(-12, 12, 0.1)
        pdf = dist.pdf(x)
        pdf_boe = dist_boe.pdf(x)

        for y, y_boe in zip(pdf, pdf_boe):
            self.assertEqual(y, y_boe)  # add assertion here

        mean_theoretical = mu + np.sqrt(2/np.pi)*(sigma2-sigma1)
        gamma_theoretical = mean_theoretical-mu
        self.assertAlmostEqual(gamma, gamma_theoretical)

    def test_parameters(self):
        self.assertRaises(TypeError, tpnorm)
        self.assertRaises(TypeError, tpnorm, loc=0.0)
        self.assertRaises(TypeError, tpnorm, loc=0.0, sigma=1.0, gamma=0.5)
        self.assertRaises(TypeError, tpnorm, loc=0.0, sigma=1.0, gamma=0.5, kind=None)
        self.assertRaises(ValueError, tpnorm, loc=0.0, sigma=1.0, gamma=0.5, kind='my_new_type')
        self.assertRaises(ValueError, tpnorm, loc=0.0, sigma=1.0, gamma=0.0, kind='inverse_scale')
        self.assertRaises(ValueError, tpnorm, loc=0.0, sigma=1.0, gamma=-1.0, kind='epsilon_skew')
        self.assertRaises(ValueError, tpnorm, loc=0.0, sigma=1.0, gamma=0.0, kind='percentile')


if __name__ == '__main__':
    unittest.main(verbosity=2)
