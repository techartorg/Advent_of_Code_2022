from unittest import TestCase

import utils.processing

class Test(TestCase):
    def test_comma_separated_integers(self):
        inTest = '1,2,3,4'
        expected = [1, 2, 3, 4]
        self.assertEqual(utils.processing.commaSeparatedIntegers(inTest), expected)
