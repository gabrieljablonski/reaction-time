from PyQt5 import QtWidgets, QtGui, QtCore
from lights_window import LightsWindow


class ControlWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))  # Dot instead of comma

        """ Create instance of lights window """
        self.lightsWindow = LightsWindow()
        self.lightsWindow.close()

        """ Window title """
        self.title = "Control Window"

        """ Default position and size of window """
        screen = QtWidgets.QApplication.desktop().screenGeometry(0)
        self.width = 1010
        self.height = 460
        self.left = (screen.right() - self.width) // 2   # Position for the window on the middle of the screen
        self.top = (screen.bottom() - self.height) // 2

        """ Creating widgets """
        self.centralWidget = QtWidgets.QWidget(self)

        # Lights Distribution
        self.groupLightsSelection = QtWidgets.QGroupBox(self.centralWidget)            # Main group
        group = self.groupLightsSelection
        self.labelLights = QtWidgets.QLabel(group)
        self.groupLightsBorder = QtWidgets.QGroupBox(group)                            # Border for checkboxes
        self.layoutLightsGridWidget = QtWidgets.QWidget(self.groupLightsBorder)        # Widget
        self.layoutLightsGrid = QtWidgets.QGridLayout(self.layoutLightsGridWidget)     # Layout
        self.lightCheckBoxes = []
        for light_n in range(self.lightsWindow.number_of_lights):
            checkbox = QtWidgets.QCheckBox(self.layoutLightsGridWidget)
            self.lightCheckBoxes.append(checkbox)
        self.buttonSelectAll = QtWidgets.QPushButton(group)                            # Activate all lights
        self.buttonDeselectAll = QtWidgets.QPushButton(group)                          # Deactivate all lights
        self.buttonSetSelection = QtWidgets.QPushButton(group)                         # Set selected lights
        #

        # Automatic Light Control
        self.groupLightsControl = QtWidgets.QGroupBox(self.centralWidget)          # Main group
        group = self.groupLightsControl
        self.treeLightOrder = QtWidgets.QTreeWidget(group)                         # List of the light order for test
        self.spinNumberLights = QtWidgets.QSpinBox(group)                          # Number of lights on test
        self.labelNumberLights = QtWidgets.QLabel(group)
        self.spinDefaultOn = QtWidgets.QDoubleSpinBox(group)                       # Default time ON for all lights
        self.labelDefaultOn = QtWidgets.QLabel(group)
        self.buttonResetDefaultOn = QtWidgets.QPushButton(group)                   # Reset all to default time ON
        self.spinDefaultInterval = QtWidgets.QDoubleSpinBox(group)                 # Default interval between lights
        self.labelDefaultInterval = QtWidgets.QLabel(group)
        self.buttonResetDefaultInterval = QtWidgets.QPushButton(group)             # Reset all to default interval
        self.buttonRandomizeOrder = QtWidgets.QPushButton(group)                   # Randomize ordering for test
        self.checkEvenDist = QtWidgets.QCheckBox(group)                            # Even distribution when randomizing
        self.spinMinimumInterval = QtWidgets.QDoubleSpinBox(group)                 # Minimum interval when randomizing
        self.labelMinimumInterval = QtWidgets.QLabel(group)
        self.spinMaximumInterval = QtWidgets.QDoubleSpinBox(group)                 # Maximum interval when randomizing
        self.labelMaximumInterval = QtWidgets.QLabel(group)
        self.buttonRandomizeIntervals = QtWidgets.QPushButton(group)               # Randomize values for intervals

        self.groupManualAdjusts = QtWidgets.QGroupBox(group)                       # Manual adjust group
        group = self.groupManualAdjusts
        self.comboChangeLight = QtWidgets.QComboBox(group)                         # Manually change light
        self.labelChangeLight = QtWidgets.QLabel(group)
        self.spinChangeTime = QtWidgets.QDoubleSpinBox(group)                      # Manually change individual time ON
        self.labelChangeTime = QtWidgets.QLabel(group)
        self.spinChangeInterval = QtWidgets.QDoubleSpinBox(group)                  # Manually change individual interval
        self.labelChangeInterval = QtWidgets.QLabel(group)
        #

        # Test Control
        self.groupTestControl = QtWidgets.QGroupBox(self.centralWidget)
        group = self.groupTestControl
        self.buttonOpenLightsWindow = QtWidgets.QPushButton(group)                 # Open the lights window
        self.spinStartDelay = QtWidgets.QSpinBox(group)                            # Delay before first light
        self.labelStartDelay = QtWidgets.QLabel(group)
        self.buttonStartSession = QtWidgets.QPushButton(group)                     # Start session
        self.buttonStopSession = QtWidgets.QPushButton(group)                      # Stop session
        self.textTestLogs = QtWidgets.QTextEdit(group)                             # Logs for test session
        self.buttonSaveLogs = QtWidgets.QPushButton(group)                         # Save logs to file
        #

        self.init_ui()

    def init_ui(self):
        """ Setting title, position and size """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        """ Fixing size of the window """
        self.setFixedSize(self.width, self.height)

        """ Set central widget """
        self.setCentralWidget(self.centralWidget)

        """ Setting geometry for widgets """
        # Lights Distribution
        self.groupLightsSelection.setGeometry(10, 10, 360, 190)
        self.labelLights.setGeometry(20, 30, 160, 16)
        self.groupLightsBorder.setGeometry(20, 40, 160, 130)
        self.layoutLightsGridWidget.setGeometry(10, 20, 160, 110)
        # Setting up the grid properly
        for index, light in enumerate(self.lightCheckBoxes):
            self.layoutLightsGrid.addWidget(light, index // int(self.lightsWindow.number_of_lights**0.5),
                                            index % int(self.lightsWindow.number_of_lights ** 0.5))  # Square matrix

        self.buttonSelectAll.setGeometry(200, 60, 150, 30)
        self.buttonDeselectAll.setGeometry(200, 100, 150, 30)
        self.buttonSetSelection.setGeometry(200, 140, 150, 30)
        #

        # Automatic Lights Control
        self.groupLightsControl.setGeometry(380, 10, 620, 440)
        self.treeLightOrder.setGeometry(10, 30, 350, 400)
        self.spinNumberLights.setGeometry(370, 30, 60, 20)
        self.labelNumberLights.setGeometry(440, 30, 150, 16)
        self.spinDefaultOn.setGeometry(370, 60, 62, 22)
        self.labelDefaultOn.setGeometry(440, 60, 221, 16)
        self.buttonResetDefaultOn.setGeometry(370, 90, 241, 20)
        self.spinDefaultInterval.setGeometry(370, 120, 62, 22)
        self.labelDefaultInterval.setGeometry(440, 120, 221, 16)
        self.buttonResetDefaultInterval.setGeometry(370, 150, 241, 20)
        self.buttonRandomizeOrder.setGeometry(520, 180, 90, 31)
        self.checkEvenDist.setGeometry(385, 185, 130, 17)
        self.spinMinimumInterval.setGeometry(370, 230, 50, 22)
        self.labelMinimumInterval.setGeometry(430, 230, 81, 16)
        self.spinMaximumInterval.setGeometry(370, 260, 50, 22)
        self.labelMaximumInterval.setGeometry(430, 260, 91, 16)
        self.buttonRandomizeIntervals.setGeometry(520, 220, 90, 70)

        self.groupManualAdjusts.setGeometry(370, 300, 241, 130)
        self.comboChangeLight.setGeometry(10, 30, 61, 22)
        self.labelChangeLight.setGeometry(80, 30, 111, 16)
        self.spinChangeTime.setGeometry(10, 60, 61, 22)
        self.labelChangeTime.setGeometry(80, 60, 91, 16)
        self.spinChangeInterval.setGeometry(10, 90, 62, 22)
        self.labelChangeInterval.setGeometry(80, 90, 121, 16)
        #

        # Test Control
        self.groupTestControl.setGeometry(10, 210, 361, 240)
        self.buttonOpenLightsWindow.setGeometry(20, 30, 151, 50)
        self.spinStartDelay.setGeometry(40, 90, 62, 22)
        self.labelStartDelay.setGeometry(110, 93, 61, 16)
        self.buttonStartSession.setGeometry(20, 120, 151, 50)
        self.buttonStopSession.setGeometry(20, 180, 151, 50)
        self.textTestLogs.setGeometry(180, 30, 171, 140)
        self.buttonSaveLogs.setGeometry(180, 180, 171, 50)
        #

        """ Setting icons """
        self.setWindowIcon(QtGui.QIcon("icons/logo.png"))
        self.buttonSelectAll.setIcon(QtGui.QIcon("icons/checked.png"))
        self.buttonDeselectAll.setIcon(QtGui.QIcon("icons/unchecked.png"))
        self.buttonSetSelection.setIcon(QtGui.QIcon("icons/accept.png"))
        self.buttonResetDefaultOn.setIcon(QtGui.QIcon("icons/undo.png"))
        self.buttonResetDefaultInterval.setIcon(QtGui.QIcon("icons/undo.png"))
        self.buttonRandomizeOrder.setIcon(QtGui.QIcon("icons/random.png"))
        self.buttonRandomizeIntervals.setIcon(QtGui.QIcon("icons/random.png"))
        self.buttonOpenLightsWindow.setIcon(QtGui.QIcon("icons/light.png"))
        self.buttonStartSession.setIcon(QtGui.QIcon("icons/start.png"))
        self.buttonStopSession.setIcon(QtGui.QIcon("icons/stop.png"))
        self.buttonSaveLogs.setIcon(QtGui.QIcon("icons/save.png"))

        """ Setting text for widgets """
        # Lights Distribution
        self.groupLightsSelection.setTitle("Lights Distribution")
        self.labelLights.setText("Select lights that will be used:")
        for index, light in enumerate(self.lightCheckBoxes):
            light.setText("%s" % str(index+1))
        self.buttonSelectAll.setText("  Select all")
        self.buttonDeselectAll.setText("  Deselect all")
        self.buttonSetSelection.setText("  Set selection")
        #

        # Automatic Lights Control
        self.groupLightsControl.setTitle("Automatic Lights Control")
        tree_header = self.treeLightOrder.headerItem()
        tree_header.setText(0, "#")
        tree_header.setText(1, "Light Number")
        tree_header.setText(2, "ON for (s)")
        tree_header.setText(3, "Following Interval (s)")
        tree_header = self.treeLightOrder.header()
        tree_header.resizeSection(0, 1)
        tree_header.resizeSection(1, 100)
        tree_header.resizeSection(2, 80)
        tree_header.resizeSection(3, 60)
        self.treeLightOrder.setRootIsDecorated(False)  # Needed to resize the header
        self.labelNumberLights.setText("Number of lights in sequence")
        self.labelDefaultOn.setText("Default time switched ON (seconds)")
        self.buttonResetDefaultOn.setText("  Reset all to default time ON")
        self.labelDefaultInterval.setText("Default interval period (seconds)")
        self.buttonResetDefaultInterval.setText("  Reset all to default interval")
        self.checkEvenDist.setText("Distribute lights evenly")
        self.buttonRandomizeOrder.setText("  Randomize\n      order")
        self.labelMinimumInterval.setText("Minimum interval")
        self.labelMaximumInterval.setText("Maximum interval")
        self.buttonRandomizeIntervals.setText("  Randomize\n   intervals")
        self.groupManualAdjusts.setTitle("Manual Adjusts")
        self.labelChangeLight.setText("Change light number")
        self.labelChangeTime.setText("Change ON time")
        self.labelChangeInterval.setText("Change interval period")
        #

        # Test Control
        self.groupTestControl.setTitle("Test Control")
        self.buttonOpenLightsWindow.setText("  Open lights window")
        self.labelStartDelay.setText("Start delay")
        self.buttonStartSession.setText("  Start session")
        self.buttonStopSession.setText("  Stop session")
        self.textTestLogs.setText("Session logs.\nWaiting for session to start.")
        self.buttonSaveLogs.setText("  Save logs")
        #

        """ Setting values for widgets """
        # Lights Distribution
        for light in self.lightCheckBoxes:
            light.setChecked(True)
        #

        # Automatic Lights Control
        self.set_spin(self.spinNumberLights, value=6, min=1)
        self.set_spin(self.spinDefaultOn, value=2, min=1, increment=0.1)
        self.set_spin(self.spinDefaultInterval, min=5, increment=0.1)
        self.checkEvenDist.setChecked(True)
        self.set_spin(self.spinMinimumInterval, value=4, min=4, max=6, increment=0.1)
        # TODO make sure the minimum is never lower than the biggest time ON
        self.set_spin(self.spinMaximumInterval, value=6, min=6, max=10, increment=0.1)
        #

        # Test Control
        self.set_spin(self.spinStartDelay, value=5, min=1, increment=1)
        #

    def set_spin(self, spin, **kwargs):  # kw: value, min, max, increment
        for key, value in kwargs.items():
            if key == "min":
                spin.setMinimum(value)              # Set minimun value for spinbox
            if key == "max":
                spin.setMaximum(value)              # Set maximun value for spinbox
            if key == "value":
                spin.setValue(value)            # Set value for spinbox
            if key == "increment":
                spin.setSingleStep(value)       # Set step size for spinbox

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = ControlWindow()
    ui.show()
    sys.exit(app.exec_())
