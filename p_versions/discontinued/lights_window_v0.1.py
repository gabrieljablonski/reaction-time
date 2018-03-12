from PyQt5 import QtWidgets, QtGui, QtCore


class LightsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        """ Window title """
        self.title = "Lights Window"

        """ Default position and size of window """
        self.left = 80
        self.top = 50
        self.width = 1600
        self.height = 900

        """ Lights """
        self.labels = []            # List of lights
        self.number_of_lights = 9
        self.light_radius = 250

        self.init_ui()

    def init_ui(self):
        """ Setting title, position and size """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        """ Setting window to frameless """
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint |      # Allow for customizing buttons
        #                     QtCore.Qt.WindowCloseButtonHint |    # Add close button
        #                     QtCore.Qt.WindowMaximizeButtonHint | # Add maximize button
        #                     QtCore.Qt.WindowMinimizeButtonHint)  # Add minimize button

        """ Maximize window and brings it to the front on secondary display, or to main one if not available """
        desktop = QtWidgets.QApplication.desktop()
        screen = desktop.screenGeometry(1)
        self.move(screen.left(), screen.top())
        self.showMaximized()
        self.activateWindow()
        self.raise_()

        """ Setting background color  """
        background_color = QtCore.Qt.black
        self.set_background_color(background_color)

        """ Setting up light grid """
        self.labels = []
        labels_color = "red"
        self.setup_grid(labels_color)

        """ Ensuring visibility for all lights """
        for label in self.labels:
            label.setVisible(True)

        """ Disable all lights """
        # self.toggle_visibility()

        """ Close on ESC press """
        close_hotkey = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        close_hotkey.activated.connect(self.quit)

    def set_background_color(self, color):
        """ Creating palette with specified color """
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def setup_grid(self, color):
        grid_layout = QtWidgets.QGridLayout()

        """ Creating round region """
        radius = self.light_radius  # In pixels
        region = QtGui.QRegion(0, 0, radius, radius, QtGui.QRegion.Ellipse)

        n = int(self.number_of_lights**0.5)  # Order of the matrix

        """ 
            Create n labels, numbered left to right, top to bottom
             Ex - n = 4:
              0  1  2  3
              4  5  6  7
              8  9 10 11
             12 13 14 15 
        """

        for light_n in range(self.number_of_lights):
            light = QtWidgets.QLabel()
            light.setMask(region)  # Set round mask for labels
            light.setStyleSheet("QLabel { background-color : %s; color : black; }" % color)
            light.setFixedSize(radius, radius)
            self.labels.append(light)
            grid_layout.addWidget(light,
                                  light_n // n,   # Row in grid
                                  light_n % n)    # Column in grid

        self.setLayout(grid_layout)

    def toggle_visibility(self, labels=None):
        if labels is not None:
            if isinstance(labels, list):   # If 'labels' is a list, toggle state for all lights listed
                for index in labels:
                    self.labels[index].setVisible(not self.labels[index].isVisible())
            elif isinstance(labels, int):  # If 'labels' is an int, toggle state for specified light
                self.labels[labels].setVisible(not self.labels[labels].isVisible())
        else:
            for label in self.labels:      # If 'labels' not specified, toggle state for all lights
                label.setVisible(not label.isVisible())

    def quit(self):
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = LightsWindow()
    ui.show()
    sys.exit(app.exec_())
