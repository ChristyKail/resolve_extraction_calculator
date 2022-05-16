import random
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

        result = extraction_calculator.ExtractionCalculator(4448, 3096, 2, ext_scale=100, squeeze=1.65).extraction_res
        self.assertEqual(result, (3752, 3096))

    def test_venice(self):

        # SV_6K_3:2_SPH_2:1_100%
        result = extraction_calculator.ExtractionCalculator(6048, 4032, 2, ext_scale=100, squeeze=1).extraction_res
        self.assertEqual(result, (6048, 3024))

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

    def test_2_1_rounding(self):

        for i in range(1, 100):

            # random even number between 1920 and 4448
            x = random.randint(int(1920 / 4), int(4448 / 4)) * 4
            y = random.randint(int(1080 / 2), int(3096 / 2)) * 2

            scale = random.randint(50, 100)
            squeeze = 1

            result = extraction_calculator.ExtractionCalculator(x, y, 2, ext_scale=scale,
                                                                squeeze=squeeze).extraction_res
            print(result)

            if result[0] % 4 == 0:
                self.assertEqual(result[0] / 2, result[1])

