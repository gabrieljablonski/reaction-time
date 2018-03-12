from collections import OrderedDict
from PyQt5 import QtWidgets, QtGui, QtCore
from lights_window import LightsWindow
import numpy as np
import os
import datetime
import time


class ControlWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))  # Dot instead of comma

        """ Create instance of lights window """
        self.lightsWindow = LightsWindow()
        # Catch ESC event from lights window
        self.lightsWindow.close_hotkey.activated.connect(self.open_lights_window)

        """ Session variable """  # Indicates testing session is ongoing
        self.on_session = False

        """ Threading for controlling the lights """
        self.autoLightControlThread = Thread()
        self.terminate_thread = False  # Flag for stopping thread
        self.signal_on = Signal()      # Turn light on signal
        self.signal_off = Signal()     # Turn light off signal
        self.signal_finished = Signal()
        self.light_index = 0

        """ Window title """
        self.title = "Control Window"

        """ Default position and size of window """
        screen = QtWidgets.QApplication.desktop().screenGeometry(0)
        self.width = 1010
        self.height = 460
        self.left = (screen.right() - self.width) // 2   # Position for the window on the middle of the screen
        self.top = (screen.bottom() - self.height) // 2

        """ Setup message box """
        self.msgBox = QtWidgets.QMessageBox()

        """ Creating widgets """
        self.centralWidget = QtWidgets.QWidget(self)

        # Lights Distribution
        self.groupLightsSelection = QtWidgets.QGroupBox(self.centralWidget)            # Main group
        group = self.groupLightsSelection
        self.labelLights = QtWidgets.QLabel(group)
        self.groupLightsBorder = QtWidgets.QGroupBox(group)                            # Border for checkboxes
        self.layoutLightsGridWidget = QtWidgets.QWidget(self.groupLightsBorder)        # Widget
        self.layoutLightsGrid = QtWidgets.QGridLayout(self.layoutLightsGridWidget)     # Layout
        # Setting light selection boxes
        self.lightCheckBoxes = []
        for light_n in range(self.lightsWindow.number_of_lights):
            checkbox = QtWidgets.QCheckBox(self.layoutLightsGridWidget)
            self.lightCheckBoxes.append(checkbox)
        self.selectedLights = OrderedDict()
        self.buttonSelectAll = QtWidgets.QPushButton(group)                            # Activate all lights
        self.buttonDeselectAll = QtWidgets.QPushButton(group)                          # Deactivate all lights
        self.buttonSetSelection = QtWidgets.QPushButton(group)                         # Set selected lights
        self.buttonClearSelection = QtWidgets.QPushButton(group)                       # Clear light selection
        #

        # Automatic Light Control
        self.groupLightsControl = QtWidgets.QGroupBox(self.centralWidget)          # Main group
        group = self.groupLightsControl
        self.treeLightOrder = QtWidgets.QTreeWidget(group)                         # List of the light order for test
        self.labelTotalTime = QtWidgets.QLabel(group)
        self.lcdTotalTime = QtWidgets.QLCDNumber(group)
        self.buttonLoadOrder = QtWidgets.QPushButton(group)                        # Load saved order list from file
        self.buttonSaveOrder = QtWidgets.QPushButton(group)                        # Save current order list to file
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
        self.buttonSetManualAdjustments = QtWidgets.QPushButton(group)
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

        """ Hotkeys """
        self.randomize_order_hotkey = QtWidgets.QShortcut(QtGui.QKeySequence("r"), self)  # Randomize all values: 'r'

        self.init_ui()

    def init_ui(self):
        """ Setting title, position and size """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        """ Fixing size of the window """
        self.setFixedSize(self.width, self.height)

        """ Set central widget """
        self.setCentralWidget(self.centralWidget)

        """ Setting pre-state for widgets """
        self.buttonClearSelection.setDisabled(True)
        self.groupLightsControl.setDisabled(True)
        self.groupManualAdjusts.setDisabled(True)
        self.groupTestControl.setDisabled(True)
        self.buttonStartSession.setDisabled(True)
        self.buttonStopSession.setDisabled(True)
        self.textTestLogs.setReadOnly(True)
        self.buttonSaveLogs.setDisabled(True)

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
        self.buttonSetSelection.setGeometry(200, 140, 70, 30)
        self.buttonClearSelection.setGeometry(280, 140, 70, 30)
        #

        # Automatic Lights Control
        self.groupLightsControl.setGeometry(380, 10, 620, 440)
        self.treeLightOrder.setGeometry(10, 30, 350, 360)
        self.labelTotalTime.setGeometry(10, 390, 100, 16)
        self.lcdTotalTime.setGeometry(50, 410, 51, 23)
        self.buttonLoadOrder.setGeometry(110, 400, 120, 31)
        self.buttonSaveOrder.setGeometry(240, 400, 120, 31)
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
        self.buttonSetManualAdjustments.setGeometry(171, 60, 60, 22)
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
        self.buttonClearSelection.setIcon(QtGui.QIcon("icons/clear.png"))
        self.buttonSaveOrder.setIcon(QtGui.QIcon("icons/save.png"))
        self.buttonLoadOrder.setIcon(QtGui.QIcon("icons/down.png"))
        self.buttonResetDefaultOn.setIcon(QtGui.QIcon("icons/undo.png"))
        self.buttonResetDefaultInterval.setIcon(QtGui.QIcon("icons/undo.png"))
        self.buttonRandomizeOrder.setIcon(QtGui.QIcon("icons/random.png"))
        self.buttonRandomizeIntervals.setIcon(QtGui.QIcon("icons/random.png"))
        self.buttonSetManualAdjustments.setIcon(QtGui.QIcon("icons/accept.png"))
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
        self.buttonSetSelection.setText("  Set")
        self.buttonClearSelection.setText("  Clear")
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
        self.labelTotalTime.setText("Total time (s):")
        self.lcdTotalTime.setDigitCount(5)
        self.lcdTotalTime.setFrameStyle(0)
        self.lcdTotalTime.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdTotalTime.display('0.0')
        self.buttonLoadOrder.setText("  Load order")
        self.buttonSaveOrder.setText("  Save order")
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
        self.buttonSetManualAdjustments.setText("    Set")
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

        """ Setting default values for widgets """
        # Lights Distribution
        for light in self.lightCheckBoxes:
            light.setChecked(True)
        #

        # Automatic Lights Control
        self.set_spin(self.spinNumberLights, value=6, min=1)
        self.set_spin(self.spinDefaultOn, value=2, min=1, increment=0.1)
        self.set_spin(self.spinDefaultInterval, min=2, increment=0.1)
        self.checkEvenDist.setChecked(True)
        self.set_spin(self.spinMinimumInterval, value=2, min=2, max=10, increment=0.1)
        self.set_spin(self.spinMaximumInterval, value=10, min=2, max=10, increment=0.1)
        self.set_spin(self.spinChangeTime, min=1, increment=0.1)
        self.set_spin(self.spinChangeInterval, min=2, max=10, increment=0.1)
        #

        # Test Control
        self.set_spin(self.spinStartDelay, value=5, min=1, increment=1)

        #

        """ Setting button connections """
        # Lights distribution
        self.buttonSelectAll.clicked.connect(self.select_all_lights)
        self.buttonDeselectAll.clicked.connect(self.deselect_all_lights)
        self.buttonSetSelection.clicked.connect(self.set_light_selection)
        self.buttonClearSelection.clicked.connect(self.clear_light_selection)
        #

        # Automatic Lights Control
        self.buttonResetDefaultOn.clicked.connect(self.reset_default_on)
        self.buttonResetDefaultInterval.clicked.connect(self.reset_default_interval)
        self.buttonRandomizeOrder.clicked.connect(self.randomize_order)
        self.buttonRandomizeIntervals.clicked.connect(self.randomize_intervals)
        self.buttonSetManualAdjustments.clicked.connect(self.set_manual_adjustments)
        self.buttonSaveOrder.clicked.connect(self.save_order)
        self.buttonLoadOrder.clicked.connect(self.load_order)
        #

        # Test Control
        self.buttonOpenLightsWindow.clicked.connect(self.open_lights_window)
        self.buttonStartSession.clicked.connect(self.start_session)
        self.buttonStopSession.clicked.connect(self.stop_session)
        #

        """ Value change events """
        self.spinNumberLights.valueChanged.connect(self.change_number_of_lights)
        self.spinMinimumInterval.valueChanged.connect(self.update_maximum_interval)  # Ensure minimum < maximum
        self.spinMaximumInterval.valueChanged.connect(self.update_minimum_interval)  # Ensure minimum < maximum

        for light in self.lightCheckBoxes:
            light.clicked.connect(self.manual_light_control)

        """ Tree selection event """
        self.treeLightOrder.currentItemChanged.connect(self.update_manual_adjust)

        """ Hotkey connections """
        self.randomize_order_hotkey.activated.connect(self.randomize_both)  # Randomize all values: 'r'

        """ Signals """
        self.signal_on.signal.connect(lambda: self.turn_light_on(self.light_index))
        self.signal_off.signal.connect(lambda: self.turn_light_off(self.light_index))
        self.signal_finished.signal.connect(self.stop_session)

    def message_box(self, msg_code, ex=None):
        """ Icon selection for message box """
        icon_information = 1
        icon_warning = 2
        icon_error = 3
        icon_question = 4
        if msg_code == "no_lights":
            text = "No lights selected."
            icon = icon_warning
            title = "Light selection"
        elif msg_code == "file_save_error":
            text = "Error saving %s." % ex
            icon = icon_warning
            title = "File error"
        elif msg_code == "file_open_error":
            text = "Error opening %s." % ex
            icon = icon_warning
            title = "File error"
        elif msg_code == "file_saved":
            text = ("%s saved successfully." % ex)
            icon = icon_information
            title = "File saved"
        else:
            text = "Unknown error."
            icon = icon_error
            title = "Error"
        self.msgBox.setText(text)
        self.msgBox.setIcon(icon)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        self.msgBox.exec_()

    def set_spin(self, spin, **kwargs):  # kws: value, min, max, increment
        for key, value in kwargs.items():
            if key == "min":
                spin.setMinimum(value)              # Set minimum value for spinbox
            if key == "max":
                spin.setMaximum(value)              # Set maximum value for spinbox
            if key == "value":
                spin.setValue(value)                # Set value for spinbox
            if key == "increment":
                spin.setSingleStep(value)           # Set step size for spinbox

    def select_all_lights(self):
        for light in self.lightCheckBoxes:  # Check all checkboxes
            light.setChecked(True)

    def deselect_all_lights(self):
        for light in self.lightCheckBoxes:  # Uncheck all checkboxes
            light.setChecked(False)

    def set_light_selection(self):
        self.selectedLights = OrderedDict()
        for light_n, light in enumerate(self.lightCheckBoxes):  # Verify selected checkboxes
            if light.isChecked():
                self.selectedLights[light_n+1] = light
            else:
                light.setDisabled(True)                       # Disable unchecked boxes
        if self.selectedLights:                               # Enable lights control
            self.buttonSetSelection.setDisabled(True)
            self.buttonSelectAll.setDisabled(True)
            self.buttonDeselectAll.setDisabled(True)
            self.buttonClearSelection.setEnabled(True)
            self.groupTestControl.setEnabled(True)
            self.groupLightsControl.setEnabled(True)

            self.create_order_tree()
        else:
            for light in self.lightCheckBoxes:                # Enable all boxes if none were checked
                light.setEnabled(True)
            self.message_box("no_lights")                     # Warning message

    def clear_light_selection(self):
        if self.lightsWindow.is_open:
            self.open_lights_window()
        for light in self.lightCheckBoxes:                    # Clear lights selection
            if not light.isEnabled():
                light.setEnabled(True)
            else:
                light.setChecked(True)
        self.buttonClearSelection.setDisabled(True)
        self.buttonSetSelection.setEnabled(True)
        self.buttonSelectAll.setEnabled(True)
        self.buttonDeselectAll.setEnabled(True)
        self.groupTestControl.setDisabled(True)

    def open_lights_window(self):
        if not self.lightsWindow.is_open:
            self.lightsWindow.open_maximized()
            self.disable_all_lights()
            self.buttonOpenLightsWindow.setText("    Close lights window")
            self.buttonStartSession.setEnabled(True)
            self.lightsWindow.is_open = True
        elif not self.on_session:
            self.lightsWindow.close()
            self.buttonOpenLightsWindow.setText("    Open lights window")
            self.buttonStartSession.setDisabled(True)
            self.lightsWindow.is_open = False

    def create_order_tree(self):
        """ Create the order list """
        self.treeLightOrder.clear()
        n_lights = self.spinNumberLights.value()
        default_time = self.spinDefaultOn.value()
        default_interval = self.spinDefaultInterval.value()
        light = iter(self.selectedLights)                     # Iterator used to add lights in the correct sequence
        if not self.treeLightOrder.topLevelItemCount():
            for light_n in range(n_lights):
                try:
                    c_light = next(light)
                except StopIteration:                         # Reset to first available light
                    light = iter(self.selectedLights)
                    c_light = next(light)
                finally:
                    # Build item and add to tree
                    tree_item = [str(light_n+1), str(c_light), "%.1f" % default_time, "%.1f" % default_interval]
                    tree_item = QtWidgets.QTreeWidgetItem(tree_item)
                    self.align_tree_item(tree_item)
                    self.treeLightOrder.addTopLevelItem(tree_item)
            # Setting display to total session time
            total_time = n_lights*(default_time + default_interval)
            self.lcdTotalTime.display("%.1f" % total_time)

    def change_number_of_lights(self):
        """ Copy tree items """
        tree_items = self.copy_tree()

        difference = self.spinNumberLights.value() - len(tree_items)
        selected_lights = list(self.selectedLights.keys())
        if difference > 0:    # Number increased
            for new_light in range(difference):
                last_light_number = int(tree_items[-1][1])                       # Light number for last item in tree
                light_index = selected_lights.index(last_light_number) + 1   # Index for subsequent light
                if light_index >= len(selected_lights):                      # If index out of bounds, back to first
                    light_index = 0
                light_number = selected_lights[light_index]
                new_tree_item = [str(int(tree_items[-1][0]) + 1), str(light_number),
                                 str(self.spinDefaultOn.value()), str(self.spinDefaultInterval.value())]
                tree_items.append(new_tree_item)

        elif difference < 0:  # Number decreased
            tree_items = tree_items[:difference]

        else:
            return

        """ Rebuild tree """
        self.build_tree(tree_items)

    def reset_default_on(self):
        default_on = self.spinDefaultOn.value()

        """ Copy and edit tree """
        tree_items = self.copy_tree()
        tree_items[:] = [[item[0], item[1], "%.1f" % default_on, item[3]] for item in tree_items]

        """ Rebuild tree """
        self.build_tree(tree_items)

    def reset_default_interval(self):
        default_interval = self.spinDefaultInterval.value()

        """ Copy and edit tree """
        tree_items = self.copy_tree()
        tree_items[:] = [[item[0], item[1], item[2], "%.1f" % default_interval] for item in tree_items]

        """ Rebuild tree """
        self.build_tree(tree_items)

    def randomize_order(self):
        """ Copy tree items """
        tree_items = self.copy_tree()

        if tree_items:
            """ Create list with selected lights, then shuffle it """
            light_order = []
            for light_n in self.selectedLights.keys():
                light_order.append(light_n)
            np.random.shuffle(light_order)
            lights = iter(light_order)                           # Iterator for shuffled lights

            """ Distribute evenly between lights when randomizing """
            if self.checkEvenDist.isChecked():
                for light_n in range(self.spinNumberLights.value()):   # Iterating through lights
                    try:
                        light = next(lights)
                    except StopIteration:                        # Reshuffle and restart iteration for
                        np.random.shuffle(light_order)           # number of lights > available lights
                        lights = iter(light_order)
                        light = next(lights)
                    finally:
                        tree_items[light_n][1] = str(light)
            else:  # Distribution completely random
                for light_n in range(self.spinNumberLights.value()):
                    # Select one light at random from the available ones
                    tree_items[light_n][1] = str(np.random.choice(light_order, 1)[0])

            """ Rebuild lights tree """
            self.build_tree(tree_items)

    def update_maximum_interval(self):
        # If the minimum interval reaches the maximum, increase maximum by 0.1
        if self.spinMinimumInterval.value() + 0.1 >= self.spinMaximumInterval.value():
            self.spinMaximumInterval.setValue(self.spinMinimumInterval.value() + 0.1)

    def update_minimum_interval(self):
        # If the maximum interval reaches the minimum, decrease minimum by 0.1
        if self.spinMaximumInterval.value() - 0.1 <= self.spinMinimumInterval.value():
            self.spinMinimumInterval.setValue(self.spinMaximumInterval.value() - 0.1)

    def randomize_intervals(self):
        """ Copy tree items """
        tree_items = self.copy_tree()

        if tree_items:
            """ Set possible intervals """
            min_interval = self.spinMinimumInterval.value()
            max_interval = self.spinMaximumInterval.value()
            possible_intervals = np.arange(min_interval, max_interval + 0.1, 0.1)

            """ Pick from possible intervals """
            tree_items[:] = [[item[0], item[1], item[2], "%.1f" % np.random.choice(possible_intervals, 1)[0]]
                             for item in tree_items]

            """ Rebuild lights tree """
            self.build_tree(tree_items)

    def randomize_both(self):
        self.randomize_order()
        self.randomize_intervals()

    def update_manual_adjust(self):
        item_selected = self.treeLightOrder.currentItem()
        if item_selected:
            self.groupManualAdjusts.setEnabled(True)
            self.comboChangeLight.clear()
            for light in self.selectedLights.keys():
                self.comboChangeLight.addItem(str(light))
            self.comboChangeLight.setCurrentText(item_selected.text(1))
            self.spinChangeTime.setValue(float(item_selected.text(2)))
            self.spinChangeInterval.setValue(float(item_selected.text(3)))
        else:
            self.groupManualAdjusts.setDisabled(True)
            self.comboChangeLight.clear()

    def set_manual_adjustments(self):
        light_selection = self.comboChangeLight.currentText()
        on_time_selection = str(self.spinChangeTime.value())
        interval_selection = str(self.spinChangeInterval.value())

        item_selected = self.treeLightOrder.currentItem()
        selected_index = int(item_selected.text(0)) - 1
        new_item = [item_selected.text(0), light_selection, on_time_selection, interval_selection]
        new_item = QtWidgets.QTreeWidgetItem(new_item)
        self.align_tree_item(new_item)

        self.treeLightOrder.takeTopLevelItem(selected_index)
        self.treeLightOrder.insertTopLevelItem(selected_index, new_item)
        if selected_index == self.treeLightOrder.topLevelItemCount() - 1:
            self.treeLightOrder.setCurrentItem(self.treeLightOrder.topLevelItem(0))

    def save_order(self):
        name = "ReactionTime_order_%s" % datetime.datetime.now().strftime("%Y%m%d")
        name = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QFileDialog(), caption="Save current order",
                                                     directory=os.path.join(os.getcwd(), name),
                                                     filter="Text files (*.txt)",
                                                     options=QtWidgets.QFileDialog.DontConfirmOverwrite)
        if name[0]:
            tree_items = self.copy_tree()
            name = os.path.split(name[0])[1]

            # Add _2, _3... if name is repeated
            file_number = 2
            t_name = name
            while os.path.exists(os.path.join(os.getcwd(), t_name)):
                t_name = name[:-4] + "_%d.txt" % file_number
                file_number += 1
            name = t_name
            try:
                file = open(name, 'w')
                date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write("# Order list for ReactionTime. Created on %s.\n" % date_time)
                file.write("# [#] [Light Number] [Time ON (s)] [Following Interval (s)]\n")
                for item in tree_items:
                    file.write("%s\t%s\t%s\t%s\n" % (item[0], item[1], item[2], item[3]))
                self.message_box("file_saved", name)
            except EnvironmentError:
                self.message_box("file_save_error", name)

    def load_order(self):
        name = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QFileDialog(), caption="Load order",
                                                     filter="Text file (*.txt)")
        if name[0]:
            name = os.path.split(name[0])[1]

            try:
                file = open(name, 'r')
                tree_items = []
                data = file.readlines()
                for line in data:
                    if line[0] != '#':
                        line = line.split()
                        tree_items.append(line)
                self.build_tree(tree_items)
                self.spinNumberLights.setValue(self.treeLightOrder.topLevelItemCount())

            except EnvironmentError:
                self.message_box("file_open_error", name)

    def disable_all_lights(self):
        for index in range(len(self.lightsWindow.labels)):
            self.turn_light_off(index)

    def start_session(self):
        if not self.autoLightControlThread.isRunning():
            self.groupLightsBorder.setDisabled(True)
            self.groupLightsControl.setDisabled(True)
            self.terminate_thread = False
            self.autoLightControlThread.start()  # Thread runs auto_light_control()
            self.buttonStopSession.setEnabled(True)
            self.buttonStartSession.setDisabled(True)
            self.buttonOpenLightsWindow.setDisabled(True)
            self.buttonClearSelection.setDisabled(True)

    def stop_session(self):
        if self.autoLightControlThread.isRunning():
            self.terminate_thread = True  # Stop thread
        self.buttonStopSession.setDisabled(True)
        self.buttonStartSession.setEnabled(True)
        self.groupLightsBorder.setEnabled(True)
        self.groupLightsControl.setEnabled(True)
        self.buttonOpenLightsWindow.setEnabled(True)
        self.buttonClearSelection.setEnabled(True)

    def manual_light_control(self):                                       # Connected when any checkbox is clicked
        if self.lightsWindow.is_open:                                     # Only when lights window is open
            light_n = self.lightCheckBoxes.index(self.sender())           # Sender: checkbox clicked
            for index in range(len(self.lightCheckBoxes)):
                if index != light_n:
                    self.turn_light_off(index)                            # Turn all other lights off/disable checkboxes
                else:
                    if self.sender().isChecked():                         # Turn correspondent light on for check
                        self.turn_light_on(index)
                    else:                                                 # Turn off for uncheck
                        self.turn_light_off(index)

    def auto_light_control(self):
        tree_items = self.copy_tree()
        time.sleep(self.spinStartDelay.value())                           # Set delay before first light
        if self.terminate_thread:
            return
        for item in tree_items:
            light_index, time_on, interval = item[1], item[2], item[3]
            self.light_index = int(light_index) - 1                       # Set light
            self.signal_on.signal.emit()                                  # Turn on light
            time.sleep(float(time_on))                                    # Keep it on for 'time_on' seconds
            if self.terminate_thread:
                self.signal_off.signal.emit()
                return
            self.signal_off.signal.emit()                                 # Turn off light
            time.sleep(float(interval))                                   # Wait 'interval' seconds before next light
            if self.terminate_thread:
                return
        self.signal_finished.signal.emit()


    def turn_light_on(self, light_index):
        self.lightCheckBoxes[light_index].setChecked(True)
        self.lightsWindow.turn_light_on(light_index)

    def turn_light_off(self, light_index):
        self.lightCheckBoxes[light_index].setChecked(False)
        self.lightsWindow.turn_light_off(light_index)

    def copy_tree(self):  # Copy items from tree and return list with them, members as strings
        tree_items = []
        for item_n in range(self.treeLightOrder.topLevelItemCount()):
            tree_item = self.treeLightOrder.topLevelItem(item_n)
            tree_item = [tree_item.text(0), tree_item.text(1), tree_item.text(2), tree_item.text(3)]
            tree_items.append(tree_item)
        return tree_items

    def build_tree(self, tree_items):  # Build tree from items given
        self.treeLightOrder.clear()
        time_count = 0                 # Counting time for total time display
        for item in tree_items:
            time_count += float(item[2]) + float(item[3])
            item = QtWidgets.QTreeWidgetItem(item)
            self.align_tree_item(item)
            self.treeLightOrder.addTopLevelItem(item)
        self.treeLightOrder.scrollToBottom()
        self.lcdTotalTime.display("%.1f" % time_count)  # Set display to total time

    def align_tree_item(self, item):
        alignment = QtCore.Qt.AlignRight
        item.setTextAlignment(1, alignment)
        item.setTextAlignment(2, alignment)
        item.setTextAlignment(3, alignment)

    def closeEvent(self, event):
        event.ignore()
        self.lightsWindow.quit()
        event.accept()


class Thread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        ui.auto_light_control()


class Signal(QtWidgets.QWidget):
    signal = QtCore.pyqtSignal()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = ControlWindow()
    ui.show()
    sys.exit(app.exec_())
