# ratios: bigger = wider
import math


class ExtractionCalculator:

    def __init__(self, capture_w, capture_h, extraction, ext_scale=100,
                 squeeze: float = 1):

        self.capture_w = capture_w
        self.capture_h = capture_h

        self.capture_ratio = self.capture_w / self.capture_h
        self.capture_ratio_desqueezed = self.capture_ratio * squeeze

        if is_extraction_calculated(extraction):

            self.ext_width, self.ext_height = extraction
            self.ext_ratio = self.ext_width / self.ext_height

        else:
            self.ext_width, self.ext_height = calculate_extraction(capture_w, capture_h, extraction, ext_scale, squeeze)
            self.ext_ratio = extraction

        self.squeeze = squeeze
        self.extraction_res = (self.ext_width, self.ext_height)

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
        return round(resolve_scale_factor, 3)


def is_extraction_calculated(extraction):
    if type(extraction) is tuple:
        return True
    else:
        return False


def calculate_extraction(capture_w, capture_h, ext_ratio, ext_scale=100, squeeze: float = 1):
    if ext_ratio == 2.39:
        print("Requested extraction is 2.39:1, this has been calculated using true DCI 2.3869:1")
        ext_ratio = 2.3869

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

    extraction_width, extraction_height = round_extraction(extraction_width, extraction_height)

    print("Extraction resolution: " + str(extraction_width) + "x" + str(extraction_height))

    return extraction_width, extraction_height


def round_extraction(ext_width, ext_height):
    ext_width = math.ceil(ext_width)
    ext_height = math.floor(ext_height)

    if ext_width % 2 != 0:
        ext_width += 1

    if ext_height % 2 != 0:
        ext_height += 1

    return ext_width, ext_height


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
    pass
