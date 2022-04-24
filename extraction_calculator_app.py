import tkinter as tk
from tkinter import messagebox
import extraction_calculator as ec


class ExtractionCalculatorApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Extraction Calculator")

        self.resizable(False, False)

        # noinspection PyTypeChecker
        self.columnconfigure(tuple(range(4)), weight=1, minsize=5, pad=10)
        # noinspection PyTypeChecker
        self.rowconfigure(tuple(range(8)), weight=1, pad=10)

        entry_box_width = 6

        # CAPTURE SECTION

        self.label_capture = tk.Label(self, text="Capture", font=("Arial", 20), pady=10)
        self.label_capture.grid(row=0, column=0, columnspan=4, sticky="ew")

        self.label_capture_width = tk.Label(self, text="Width")
        self.entry_capture_width = tk.Entry(self, width=entry_box_width)

        self.label_capture_height = tk.Label(self, text="Height")
        self.entry_capture_height = tk.Entry(self, width=entry_box_width)

        self.label_capture_width.grid(row=1, column=0, sticky="e")
        self.entry_capture_width.grid(row=1, column=1, sticky="w")
        self.label_capture_height.grid(row=1, column=2, sticky="e")
        self.entry_capture_height.grid(row=1, column=3, sticky="w")

        self.label_squeeze = tk.Label(self, text="Squeeze")
        self.entry_squeeze = tk.Entry(self, width=entry_box_width)
        self.entry_squeeze.insert(0, "1")

        self.label_squeeze.grid(row=2, column=0, sticky="e")
        self.entry_squeeze.grid(row=2, column=1, sticky="w")

        # EXTRACTION SECTION

        self.label_extraction = tk.Label(self, text="Extraction", font=("Arial", 20), pady=10)
        self.label_extraction.grid(row=3, column=0, columnspan=4, sticky="ew")

        self.label_ratio = tk.Label(self, text="Ratio")
        self.entry_ratio = tk.Entry(self, width=entry_box_width)

        self.label_scale = tk.Label(self, text="Scale")
        self.entry_scale = tk.Entry(self, width=entry_box_width)
        self.entry_scale.insert(0, "100")

        self.label_ratio.grid(row=4, column=0, sticky="e")
        self.entry_ratio.grid(row=4, column=1, sticky="w")
        self.label_scale.grid(row=4, column=2, sticky="e")
        self.entry_scale.grid(row=4, column=3, sticky="w")

        self.label_extraction_width = tk.Label(self, text="Width")
        self.entry_extraction_width = tk.Entry(self, width=entry_box_width)
        self.label_extraction_height = tk.Label(self, text="Height")
        self.entry_extraction_height = tk.Entry(self, width=entry_box_width)

        self.label_extraction_width.grid(row=5, column=0, sticky="e")
        self.entry_extraction_width.grid(row=5, column=1, sticky="w")
        self.label_extraction_height.grid(row=5, column=2, sticky="e")
        self.entry_extraction_height.grid(row=5, column=3, sticky="w")

        # CALCULATE BUTTON

        self.button_calculate = tk.Button(self, text="Calculate", command=self.calculate, height=2, width=8, padx=10)
        self.button_calculate.grid(row=7, column=0, columnspan=4, sticky="ew")

        # RESULT SECTION

        self.label_fit = tk.Label(self, text="Fit", font=("Arial", 20), pady=10)
        self.label_fit_value = tk.Label(self, text="", font=("Arial", 20), pady=10)

        self.label_crop = tk.Label(self, text="Crop", font=("Arial", 20), pady=10)
        self.label_crop_value = tk.Label(self, text="", font=("Arial", 20), pady=10)

        self.label_fit.grid(row=8, column=0, sticky="e")
        self.label_fit_value.grid(row=8, column=1, sticky="w")
        self.label_crop.grid(row=8, column=2, sticky="e")
        self.label_crop_value.grid(row=8, column=3, sticky="w")

    def calculate(self):

        try:
            capture_width = int(self.entry_capture_width.get())
            capture_height = int(self.entry_capture_height.get())
            squeeze = float(self.entry_squeeze.get())
        except ValueError:
            print("Invalid capture width, height, or squeeze")
            return

        try:
            ratio = float(self.entry_ratio.get())
            scale = float(self.entry_scale.get())
        except ValueError:
            calculate_from_ratio = False
        else:
            calculate_from_ratio = True

        if calculate_from_ratio:

            ext_w, ext_h = ec.calculate_extraction(capture_width, capture_height, ratio, ext_scale=scale, squeeze=squeeze)
            self.entry_extraction_width.delete(0, tk.END)
            self.entry_extraction_width.insert(0, ext_w)
            self.entry_extraction_height.delete(0, tk.END)
            self.entry_extraction_height.insert(0, ext_h)

            fit = ec.ExtractionCalculator(capture_width, capture_height, ratio, ext_scale=scale, squeeze=squeeze).resolve_scale('fit')
            crop = ec.ExtractionCalculator(capture_width, capture_height, ratio, ext_scale=scale, squeeze=squeeze).resolve_scale('crop')

        else:
            try:
                ext_w = int(self.entry_extraction_width.get())
                ext_h = int(self.entry_extraction_height.get())
            except ValueError:
                print("Invalid extraction width or height")
                return

            self.entry_scale.delete(0, tk.END)
            self.entry_ratio.delete(0, tk.END)

            fit = ec.ExtractionCalculator(capture_width, capture_height, (ext_w, ext_h), squeeze=squeeze).resolve_scale('fit')
            crop = ec.ExtractionCalculator(capture_width, capture_height, (ext_w, ext_h), squeeze=squeeze).resolve_scale('crop')

        self.label_fit_value.config(text=fit)
        self.label_crop_value.config(text=crop)


if __name__ == "__main__":
    app = ExtractionCalculatorApp()
    app.mainloop()
