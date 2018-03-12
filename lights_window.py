# Copyright 2018 GABRIEL JABLONSKI
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from PyQt5 import QtWidgets, QtGui, QtCore


class LightsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        """ State variable """
        self.is_open = False
        self.can_close = True

        """ Window title """
        self.title = "Lights Window"

        """ Default position and size of window """
        self.left_ = 80
        self.top_ = 50
        self.width_ = 1920
        self.height_ = 1080

        """ Lights """
        self.lights = []            # List of lights
        self.labels_on_top = []     # Labels that will sit on top of the lights, "lighting" them on and off
        self.number_of_lights = 9
        self.light_radius = 250
        self.top_label_radius = 225
        self.lights_color = "white"

        """ Signals """
        # Close signal
        self.close_signal = Signal()

        """ Hotkeys """
        # Emit close signal on ESC press
        self.close_hotkey = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        self.close_hotkey.activated.connect(self.close_signal.signal.emit)

        self.init_ui()

    def init_ui(self):
        """ Setting title, position, and size for main window """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left_, self.top_, self.width_, self.height_)

        """ Setting window to frameless """
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint |      # Allow for customizing buttons
        #                     QtCore.Qt.WindowCloseButtonHint |    # Add close button
        #                     QtCore.Qt.WindowMaximizeButtonHint | # Add maximize button
        #                     QtCore.Qt.WindowMinimizeButtonHint)  # Add minimize button

        """ Maximize window and brings it to the front on secondary display, or to main one if not available """
        desktop = QtWidgets.QApplication.desktop()
        screen = desktop.screenGeometry(1)
        if not screen.width():                 # If secondary display is not found, width() == 0
            screen = desktop.screenGeometry(0)
        self.left_ = screen.left()
        self.top_ = screen.top()
        self.width_ = screen.width()
        self.height_ = screen.height()
        self.light_radius = 0.13 * self.width_                  # ~250px on 1920x1080 display
        self.top_label_radius = 0.117 * self.width_             # ~225px on 1920x1080 display
        self.setGeometry(self.left_, self.top_, self.width_, self.height_)

        # self.open_maximized()
        # self.close()

        """ Setting background color  """
        background_color = QtCore.Qt.black
        self.set_background_color(background_color)

        """ Setting up light grid """
        self.lights = []
        self.labels_on_top = []
        self.setup_grid()

        """ Ensuring visibility for all lights """
        for light in self.lights:
            light.setVisible(True)

    def set_background_color(self, color):
        """ Creating palette with specified color """
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def setup_grid(self):
        grid_layout = QtWidgets.QGridLayout()

        """ Creating round region """
        l_radius = self.light_radius         # In pixels
        tl_radius = self.top_label_radius
        radii_diff = l_radius - tl_radius    # Information needed for proper positioning
        x_center = self.width()//3
        y_center = self.height()//3
        light_region = QtGui.QRegion((x_center-l_radius)//2, (y_center-l_radius)//2, l_radius, l_radius,
                                     QtGui.QRegion.Ellipse)
        top_label_region = QtGui.QRegion((x_center-l_radius + radii_diff)//2, (y_center - l_radius + radii_diff)//2,
                                         tl_radius, tl_radius, QtGui.QRegion.Ellipse)

        n = int(self.number_of_lights**0.5)  # Order of the matrix

        """ 
            Create n lights, numbered left to right, top to bottom
             Ex - n = 4:
              0  1  2  3
              4  5  6  7
              8  9 10 11
             12 13 14 15 
        """

        for light_n in range(self.number_of_lights):
            light = QtWidgets.QLabel()
            light.setMask(light_region)  # Set round mask for lights
            light.setStyleSheet("QLabel { background-color: black }")
            # light.setFixedSize(l_radius, l_radius)

            top_label = QtWidgets.QLabel()
            top_label.setMask(top_label_region)
            top_label.setStyleSheet("QLabel { background-color: black }")
            # top_label.setFixedSize(tl_radius, tl_radius)

            self.lights.append(light)
            self.labels_on_top.append(top_label)
            grid_layout.addWidget(light,
                                  light_n // n,   # Row in grid
                                  light_n % n)    # Column in grid
            grid_layout.addWidget(top_label,
                                  light_n // n,
                                  light_n % n)

        self.setLayout(grid_layout)

    def turn_light_on(self, light_index):   # Receives an index for a light, then turns it on
        label_on_top = self.labels_on_top[light_index]
        label_on_top.setStyleSheet("QLabel { background-color: %s }" % self.lights_color)

    def turn_light_off(self, light_index):  # Receives an index for a light, then turns it off
        label_on_top = self.labels_on_top[light_index]
        label_on_top.setStyleSheet("QLabel { background-color: black }")

    def enable_light(self, light_index):  # Enable circumference
        light = self.lights[light_index]
        light.setStyleSheet("QLabel { background-color: %s }" % self.lights_color)
        self.turn_light_off(light_index)

    def disable_light(self, light_index):  # Disable circumference
        light = self.lights[light_index]
        light.setStyleSheet("QLabel { background-color: black }")
        self.turn_light_off(light_index)

    def open_maximized(self):
        self.showMaximized()
        self.activateWindow()
        self.raise_()

    def closeEvent(self, event):
        event.ignore()
        self.close_signal.signal.emit()
        if self.can_close:
            event.accept()


class Signal(QtWidgets.QWidget):
    signal = QtCore.pyqtSignal()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = LightsWindow()
    # ui.show()
    sys.exit(app.exec_())
