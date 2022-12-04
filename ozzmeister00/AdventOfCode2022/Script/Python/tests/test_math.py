from unittest import TestCase

import utils.math


class Test(TestCase):
    def test_clamp(self):
        testValues = {(2, 3, 4): 3,
                      (3, 2, 4): 3,
                      (4, 2, 3): 3}

        for test, answer in testValues.items():
            self.assertEqual(utils.math.clamp(test[0], test[1], test[2]),
                             answer, msg="Failed to properly clamp {} to {}".format(test, answer))

    def test_saturate(self):
        testValues = {-1.0: 0.0,
                      0.5: 0.5,
                      1.5: 1.0}

        for test, answer in testValues.items():
            self.assertEqual(utils.math.saturate(test), answer,
                             msg="Failed to saturate {} to expected {}".format(test, answer))
