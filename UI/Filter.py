from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QLabel


class Filter(QSlider):
    defaultK = 0
    filterCount = 0

    def __init__(self):
        super(Filter, self).__init__()
        self.numA = 0
        self.k = round(self.numA*0.6)

        # Label for the slider
        self.k_lbl = QLabel(str(self.k))

        # Increase the number of filters created
        Filter.filterCount += 1

        # Slider for the first OpenCV filter, with min, max, default and step values
        self.thresh_sld = QSlider(Qt.Horizontal, self)
        self.thresh_sld.setMinimum(round(self.numA*0.6))
        self.thresh_sld.setMaximum(self.numA)
        self.thresh_sld.setValue(self.k)


    def changeValue(self, value):
        # Function for setting the value of k1
        self.k = value
        self.thresh_sld.setValue(self.k)
        self.k_lbl.setText(str(self.k))

    def changeMax(self, value):
        self.k = round(value*0.6)
        self.thresh_sld.setMinimum(round(value * 0.6))
        self.thresh_sld.setMaximum(value)
        self.thresh_sld.setValue(self.k)