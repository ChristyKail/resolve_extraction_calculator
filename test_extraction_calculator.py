import unittest
import extraction_calculator


class TestExtractionCalculator(unittest.TestCase):

    def test_alf(self):

        # ALF_OG_SPH_2:1_100%
        result = extraction_calculator.ExtractionCalculator(4448, 3096, 2, ext_scale=100, squeeze=1).extraction_res
        self.assertEqual(result, (4448, 2224))

        # ALF_OG_SPH_1.77_100%
        result = extraction_calculator.ExtractionCalculator(4448, 3096, 16 / 9, ext_scale=100, squeeze=1).extraction_res
        self.assertEqual(result, (4448, 2502))

        # ALF_OG_SPH_1.77_90%
        result = extraction_calculator.ExtractionCalculator(4448, 3096, 16 / 9, ext_scale=90, squeeze=1).extraction_res
        self.assertEqual(result, (4004, 2252))

        # ALF_OG_ANA_2X_2:1_100%
        result = extraction_calculator.ExtractionCalculator(4448, 3096, 2, ext_scale=100, squeeze=2).extraction_res
        self.assertEqual(result, (3096, 3096))

    def test_venice(self):

        # SV_6K_3:2_SPH_2:1_100%
        result = extraction_calculator.ExtractionCalculator(6048, 4032, 2, ext_scale=100, squeeze=1).extraction_res
        self.assertEqual(result, (6048, 3024))

        # SV_6K_3:2_SPH_2.39_100%
        result = extraction_calculator.ExtractionCalculator(6048, 4032, 2.39, ext_scale=100, squeeze=1).extraction_res
        self.assertEqual(result, (6048, 2532))

        # TBORN ANA
        result = extraction_calculator.ExtractionCalculator(6048, 4032, 2.39, ext_scale=100, squeeze=1.8).extraction_res
        self.assertEqual(result, (5354, 4032))

    def test_gc_extractions(self):

        result = extraction_calculator.ExtractionCalculator(5120, 2700, 2.3869, ext_scale=100, squeeze=1).extraction_res
        self.assertEqual(result, (5120, 2146))

        result = extraction_calculator.ExtractionCalculator(6016, 3200, 2.3869, ext_scale=100, squeeze=1).extraction_res
        self.assertEqual(result, (6016, 2520))

        result = extraction_calculator.ExtractionCalculator(6144, 3160, 2.3869, ext_scale=100, squeeze=1).extraction_res
        self.assertEqual(result, (6144, 2574))