import unittest

from core.sacred_metrics import (
    INV_PHI,
    PHI,
    coherence_fraction,
    consecutive_ratio,
    fibonacci,
    inverse_phi_weights,
    phi_ratio_error,
)


class TestSacredMetrics(unittest.TestCase):
    def test_phi_identity(self):
        self.assertAlmostEqual(PHI * PHI, PHI + 1.0, places=12)
        self.assertAlmostEqual(INV_PHI, PHI - 1.0, places=12)

    def test_fibonacci_and_convergence(self):
        self.assertEqual([fibonacci(i) for i in range(8)], [0, 1, 1, 2, 3, 5, 8, 13])
        self.assertLess(phi_ratio_error(20), phi_ratio_error(5))
        self.assertAlmostEqual(consecutive_ratio(20), PHI, places=6)

    def test_inverse_phi_weights_are_normalized(self):
        weights = inverse_phi_weights(4)
        self.assertAlmostEqual(sum(weights), 1.0, places=12)
        self.assertGreater(weights[0], weights[1])
        self.assertEqual(inverse_phi_weights(0), [])

    def test_coherence_fraction_is_observable(self):
        self.assertAlmostEqual(coherence_fraction(3, 5), 0.6)
        with self.assertRaises(ValueError):
            coherence_fraction(6, 5)


if __name__ == "__main__":
    unittest.main()
