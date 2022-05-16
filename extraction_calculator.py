
import math

__version__ = '0.2.0 beta'


class ExtractionCalculator:

    def __init__(self, capture_w, capture_h, extraction, ext_scale=100,
                 squeeze: float = 1):

        self.capture_w = capture_w
        self.capture_h = capture_h
        self.squeeze = squeeze
        self.ext_scale = ext_scale

        self.capture_ratio = self.capture_w / self.capture_h
        self.capture_ratio_desqueezed = self.capture_ratio * squeeze

        if is_extraction_calculated(extraction):

            self.ext_width, self.ext_height = extraction
            self.ext_ratio = self.ext_width / self.ext_height

        else:
            self.ext_ratio = extraction
            self.ext_width, self.ext_height = calculate_extraction(capture_w, capture_h, extraction, ext_scale, squeeze)
            self.ext_width, self.ext_height = self.round_extraction()

        self.extraction_res = (self.ext_width, self.ext_height)

    def __repr__(self):

        if self.squeeze == 1:
            ana_squeeze = "SPH"
        else:
            ana_squeeze = f"ANA_{self.squeeze}x"

        compiled = f'{self.capture_w}x{self.capture_h}_{ana_squeeze}_{self.ext_ratio}_{self.ext_scale} -> {self.ext_width}x{self.ext_height}'

        return '{}{}{}'.format(PrintColors.OKGREEN, compiled, PrintColors.ENDC)

    def resolve_scale(self, mode):

        # calculate window resolution

        print(f"{mode} mode")

        window_width = self.capture_w
        window_height = self.capture_h

        if mode == "crop":

            if self.capture_ratio_desqueezed < (16 / 9):
                print("Currently fit to width in Resolve")
                window_height = self.capture_w / (16 / 9) * self.squeeze

            elif self.capture_ratio_desqueezed > (16 / 9):
                print("Currently fit to height in Resolve")
                window_width = self.capture_h * (16 / 9) / self.squeeze

        elif mode == "fit":

            # unsure of this one!
            if self.capture_ratio_desqueezed < (16 / 9):
                print("Currently fit to height in Resolve")
                window_width = self.capture_h * (16 / 9) / self.squeeze

            elif self.capture_ratio_desqueezed > (16 / 9):
                print("Currently fit to width in Resolve")
                window_height = self.capture_w / (16 / 9) * self.squeeze

        else:
            print("Invalid mode")
            raise ValueError("Invalid mode")

        print("Window resolution: " + str(window_width) + "x" + str(window_height))

        # calculate scale factor to fit extraction to window

        if self.ext_ratio > (16 / 9):
            print("Extraction is wider than window")
            resolve_scale_factor = window_width / self.ext_width
        else:
            print("Extraction is narrower than window")
            resolve_scale_factor = window_height / self.ext_height

        print("{}Resolve scale factor: {}{}".format(PrintColors.OKGREEN, resolve_scale_factor, PrintColors.ENDC))
        return resolve_scale_factor

    def round_extraction(self):

        # check if we should give width or height priority
        width_fraction = self.ext_width / self.capture_w
        height_fraction = self.ext_height / self.capture_h

        if width_fraction > height_fraction:
            # give width priority
            rounded_w = round_to_nearest_even(self.ext_width)

            rounded_h = rounded_w / self.ext_ratio * self.squeeze
            rounded_h = round_to_nearest_even(rounded_h, 'round')

        else:
            # give height priority
            rounded_h = round_to_nearest_even(self.ext_height)

            rounded_w = rounded_h * self.ext_ratio / self.squeeze
            rounded_w = round_to_nearest_even(rounded_w, 'round')

        if rounded_w > self.capture_w or rounded_h > self.capture_h:
            raise ValueError("Extraction dimensions are too large {} {}".format(rounded_w, rounded_h))

        return rounded_w, rounded_h


def is_extraction_calculated(extraction):
    if type(extraction) is tuple:
        return True
    else:
        return False


def calculate_extraction(capture_w, capture_h, ext_ratio, ext_scale=100, squeeze: float = 1):
    if ext_ratio == 2.39:
        print("Requested extraction is 2.39:1, but true DCI widescreen is 2.3869:1")

    ext_ratio_squeezed = ext_ratio / squeeze
    capture_ratio = capture_w / capture_h

    ext_scale = ext_scale / 100

    if capture_ratio < ext_ratio_squeezed:

        extraction_width = capture_w
        extraction_height = capture_w / ext_ratio_squeezed

    else:

        extraction_width = capture_h * ext_ratio_squeezed
        extraction_height = capture_h

    extraction_height = extraction_height * ext_scale
    extraction_width = extraction_width * ext_scale

    return extraction_width, extraction_height


def round_to_nearest_even(value, mode="round"):
    value = value / 2

    if mode == "ceil":
        value = math.ceil(value)
    elif mode == "floor":
        value = math.floor(value)
    else:
        value = round(value)

    value = value * 2
    return value


class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == "__main__":
    print(ExtractionCalculator(4448, 3096, 2, squeeze=1.65))
