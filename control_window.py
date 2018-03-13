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

from collections import OrderedDict
from PyQt5 import QtWidgets, QtGui, QtCore
from lights_window import LightsWindow
from random import shuffle, choice
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
        self.lightsWindow.close_signal.signal.connect(self.open_lights_window)

        """ State variables """
        self.on_session = False  # Indicates testing session is ongoing
        self.last_session_saved = True

        """ Threading for controlling the lights """
        self.autoLightControlThread = Thread(self.auto_light_control)
        self.terminate_thread = False     # Flag for stopping thread
        self.start_datetime = 0           # Datetime of session start
        self.signal_countdown = Signal()  # Update countdown signal
        self.signal_on = Signal()         # Turn light on signal
        self.signal_off = Signal()        # Turn light off signal
        self.signal_finished = Signal()   # Session finish
        self.light_index = 0              # Current light being controlled
        self.current_in_sequence = 0      # Current number in sequence
        self.remaining_time = 0           # Total remaining time
        self.time_until_next_light = 0    # Time before next light is lit

        """ Window title """
        self.title = "ReactionTime v1.0"

        """ Default position and size of window """
        screen = QtWidgets.QApplication.desktop().screenGeometry(0)
        self.width = 930
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
        # Setting light selection boxes
        self.lightCheckBoxes = []
        for light_n in range(self.lightsWindow.number_of_lights):
            checkbox = QtWidgets.QCheckBox(self.layoutLightsGridWidget)
            self.lightCheckBoxes.append(checkbox)
        self.selectedLights = OrderedDict()                            # Dictionary with marked checkboxes
        # Keys are the light number (1, 2, 3, ..., n^2)
        # Values are the checkbox objects
        self.buttonSelectAll = QtWidgets.QPushButton(group)            # Activate all lights
        self.buttonDeselectAll = QtWidgets.QPushButton(group)          # Deactivate all lights
        self.buttonSetSelection = QtWidgets.QPushButton(group)         # Set selected lights
        self.buttonClearSelection = QtWidgets.QPushButton(group)       # Clear light selection
        #

        # Automatic Light Control
        self.groupLightsControl = QtWidgets.QGroupBox(self.centralWidget)          # Main group
        group = self.groupLightsControl
        self.treeLightSequence = QtWidgets.QTreeWidget(group)                      # List of the light sequence
        self.labelTotalTime = QtWidgets.QLabel(group)
        self.lcdTotalTime = QtWidgets.QLCDNumber(group)
        self.buttonLoadSequence = QtWidgets.QPushButton(group)                     # Load saved sequence list from file
        self.buttonSaveSequence = QtWidgets.QPushButton(group)                     # Save current sequence list to file
        self.spinNumberBlocks = QtWidgets.QSpinBox(group)                          # Number of lights on test
        self.labelNumberTestBlocks = QtWidgets.QLabel(group)
        self.spinBlockLength = QtWidgets.QSpinBox(group)                           # Length for each block in seconds
        self.labelBlockLength = QtWidgets.QLabel(group)
        self.spinDefaultOn = QtWidgets.QSpinBox(group)                       # Default time ON for all lights
        self.labelDefaultOn = QtWidgets.QLabel(group)
        self.spinDefaultTurnOnInstant = QtWidgets.QSpinBox(group)            # Default instant to turn lights on
        self.labelDefaultTurnOnInstant = QtWidgets.QLabel(group)
        self.buttonResetDefaultTurnOnInstant = QtWidgets.QPushButton(group)  # Reset all to default interval
        self.buttonShuffleSequence= QtWidgets.QPushButton(group)                   # Shuffle sequence
        self.checkEvenDist = QtWidgets.QCheckBox(group)                            # Even distribution when randomizing
        self.spinMinimumInstant = QtWidgets.QSpinBox(group)                 # Smallest instant when randomizing
        self.labelMinimumInstant = QtWidgets.QLabel(group)
        self.spinMaximumInstant = QtWidgets.QSpinBox(group)                 # Largest instant when randomizing
        self.labelMaximumInstant = QtWidgets.QLabel(group)
        self.buttonShuffleInstants = QtWidgets.QPushButton(group)               # Shuffle values for intervals

        self.groupManualAdjusts = QtWidgets.QGroupBox(group)                       # Manual adjust group
        group = self.groupManualAdjusts
        self.comboChangeLight = QtWidgets.QComboBox(group)                         # Manually change light
        self.labelChangeLight = QtWidgets.QLabel(group)
        self.spinChangeTurnOnInstant = QtWidgets.QSpinBox(group)            # Manually change individual turn on instant
        self.labelChangeTurnOnInstant = QtWidgets.QLabel(group)
        self.buttonSetManualAdjustments = QtWidgets.QPushButton(group)
        #

        # Test Control
        self.groupTestControl = QtWidgets.QGroupBox(self.centralWidget)
        group = self.groupTestControl
        self.buttonOpenLightsWindow = QtWidgets.QPushButton(group)                 # Open the lights window
        self.buttonStartSession = QtWidgets.QPushButton(group)                     # Start session
        self.buttonStopSession = QtWidgets.QPushButton(group)                      # Stop session
        self.lcdTimeRemaining = QtWidgets.QLCDNumber(group)                        # Countdown for remaining time
        self.labelTimeRemaining = QtWidgets.QLabel(group)
        self.lcdNextLight = QtWidgets.QLCDNumber(group)                            # Time until next light
        self.labelNextLight = QtWidgets.QLabel(group)
        self.textTestLogs = QtWidgets.QTextEdit(group)                             # Logs for test session
        self.buttonSaveLogs = QtWidgets.QPushButton(group)                         # Save logs to file
        #

        """ Hotkeys """
        self.shuffle_sequence_hotkey = QtWidgets.QShortcut(QtGui.QKeySequence("r"), self)  # Shuffle all values: 'r'

        self.init_ui()

    def init_ui(self):
        """ Setting title, position, and size of main window """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        """ Fixing size of the window """
        self.setFixedSize(self.width, self.height)

        """ Set central widget """
        self.setCentralWidget(self.centralWidget)

        """ Setting default state for widgets """
        self.buttonClearSelection.setDisabled(True)
        self.groupLightsControl.setDisabled(True)
        self.spinBlockLength.setDisabled(True)
        self.spinMinimumInstant.setDisabled(True)
        self.spinMaximumInstant.setDisabled(True)
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
        self.groupLightsControl.setGeometry(380, 10, 540, 440)
        self.treeLightSequence.setGeometry(10, 30, 270, 360)
        self.buttonLoadSequence.setGeometry(10, 400, 130, 31)
        self.buttonSaveSequence.setGeometry(150, 400, 130, 31)
        self.spinNumberBlocks.setGeometry(290, 30, 60, 22)
        self.labelNumberTestBlocks.setGeometry(360, 30, 150, 16)
        self.spinBlockLength.setGeometry(290, 60, 60, 22)
        self.labelBlockLength.setGeometry(360, 60, 150, 16)
        self.labelTotalTime.setGeometry(290, 100, 100, 16)
        self.lcdTotalTime.setGeometry(360, 90, 61, 30)
        self.spinDefaultOn.setGeometry(290, 130, 62, 22)
        self.labelDefaultOn.setGeometry(360, 130, 221, 16)
        self.spinDefaultTurnOnInstant.setGeometry(290, 160, 62, 22)
        self.labelDefaultTurnOnInstant.setGeometry(360, 160, 221, 16)
        self.buttonResetDefaultTurnOnInstant.setGeometry(290, 190, 240, 31)
        self.buttonShuffleSequence.setGeometry(440, 230, 90, 31)
        self.checkEvenDist.setGeometry(295, 235, 130, 17)
        self.spinMinimumInstant.setGeometry(290, 280, 50, 22)
        self.labelMinimumInstant.setGeometry(350, 280, 81, 16)
        self.spinMaximumInstant.setGeometry(290, 310, 50, 22)
        self.labelMaximumInstant.setGeometry(350, 310, 91, 16)
        self.buttonShuffleInstants.setGeometry(440, 270, 90, 70)

        self.groupManualAdjusts.setGeometry(290, 340, 241, 90)
        self.comboChangeLight.setGeometry(10, 30, 61, 22)
        self.labelChangeLight.setGeometry(80, 30, 111, 16)
        self.spinChangeTurnOnInstant.setGeometry(10, 61, 62, 22)
        self.labelChangeTurnOnInstant.setGeometry(80, 61, 121, 16)
        self.buttonSetManualAdjustments.setGeometry(201, 30, 30, 50)
        #

        # Test Control
        self.groupTestControl.setGeometry(10, 210, 361, 240)
        self.buttonOpenLightsWindow.setGeometry(20, 30, 151, 60)
        self.buttonStartSession.setGeometry(20, 100, 151, 60)
        self.buttonStopSession.setGeometry(20, 170, 151, 60)
        self.lcdTimeRemaining.setGeometry(290, 30, 61, 31)
        self.labelTimeRemaining.setGeometry(180, 40, 121, 16)
        self.lcdNextLight.setGeometry(300, 60, 51, 31)
        self.labelNextLight.setGeometry(180, 70, 121, 16)
        self.textTestLogs.setGeometry(180, 100, 171, 60)
        self.buttonSaveLogs.setGeometry(180, 170, 171, 60)
        #

        """ Setting icons """
        self.setWindowIcon(QtGui.QIcon("icons/logo.png"))
        self.buttonSelectAll.setIcon(QtGui.QIcon("icons/checked.png"))
        self.buttonDeselectAll.setIcon(QtGui.QIcon("icons/unchecked.png"))
        self.buttonSetSelection.setIcon(QtGui.QIcon("icons/accept.png"))
        self.buttonClearSelection.setIcon(QtGui.QIcon("icons/clear.png"))
        self.buttonSaveSequence.setIcon(QtGui.QIcon("icons/save.png"))
        self.buttonLoadSequence.setIcon(QtGui.QIcon("icons/down.png"))
        self.buttonResetDefaultTurnOnInstant.setIcon(QtGui.QIcon("icons/undo.png"))
        self.buttonShuffleSequence.setIcon(QtGui.QIcon("icons/random.png"))
        self.buttonShuffleInstants.setIcon(QtGui.QIcon("icons/random.png"))
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
        tree_header = self.treeLightSequence.headerItem()
        tree_header.setText(0, "Block Number")
        tree_header.setText(1, "Light Number")
        tree_header.setText(2, "Turn on at (s)")
        tree_header = self.treeLightSequence.header()
        tree_header.resizeSection(0, 90)
        tree_header.resizeSection(1, 90)
        tree_header.resizeSection(2, 70)
        self.treeLightSequence.setRootIsDecorated(False)  # Needed to resize the header
        self.labelTotalTime.setText("Total time (s):")
        self.lcdTotalTime.setDigitCount(4)
        self.lcdTotalTime.setFrameStyle(0)
        self.lcdTotalTime.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdTotalTime.display('00')
        self.buttonLoadSequence.setText("  Load sequence")
        self.buttonSaveSequence.setText("  Save sequence")
        self.labelNumberTestBlocks.setText("Number of test blocks")
        self.labelBlockLength.setText("Block length (s)")
        self.labelDefaultOn.setText("Time ON (s)")
        self.labelDefaultTurnOnInstant.setText("Default turn on instant (s)")
        self.buttonResetDefaultTurnOnInstant.setText("  Reset all to default\n    turn on instant")
        self.checkEvenDist.setText("Distribute lights evenly")
        self.buttonShuffleSequence.setText("  Shuffle\n  sequence")
        self.labelMinimumInstant.setText("Smallest instant")
        self.labelMaximumInstant.setText("Largest instant")
        self.buttonShuffleInstants.setText("   Shuffle\n   instants")
        self.groupManualAdjusts.setTitle("Manual Adjusts")
        self.labelChangeLight.setText("Change light number")
        self.labelChangeTurnOnInstant.setText("Change turn on instant")
        #

        # Test Control
        self.groupTestControl.setTitle("Test Control")
        self.buttonOpenLightsWindow.setText("  Open lights window")
        self.buttonStartSession.setText("  Start session")
        self.buttonStopSession.setText("  Stop session")
        self.labelTimeRemaining.setText("Total remaining time (s):")
        self.lcdTimeRemaining.setDigitCount(6)
        self.lcdTimeRemaining.setFrameStyle(0)
        self.lcdTimeRemaining.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdTimeRemaining.display('0.0')
        self.labelNextLight.setText("Time until next light (s):")
        self.lcdNextLight.setDigitCount(5)
        self.lcdNextLight.setFrameStyle(0)
        self.lcdNextLight.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNextLight.display('0.0')
        self.textTestLogs.setText("Session logs.\nWaiting for session to start.")
        self.buttonSaveLogs.setText("  Save logs")
        #

        """ Setting default values for widgets """
        # Lights Distribution
        for light in self.lightCheckBoxes:
            light.setChecked(True)
        #

        # Automatic Lights Control
        self.set_spin(self.spinNumberBlocks, value=6, min=1)
        self.set_spin(self.spinBlockLength, value=15)
        self.set_spin(self.spinDefaultOn, value=5, min=1, max=5)
        self.set_spin(self.spinDefaultTurnOnInstant, value=7, min=5, max=10)
        self.checkEvenDist.setChecked(True)
        self.set_spin(self.spinMinimumInstant, value=5)
        self.set_spin(self.spinMaximumInstant, value=10)
        self.set_spin(self.spinChangeTurnOnInstant, min=5, max=10)
        #

        """ Setting button connections """
        # Lights distribution
        self.buttonSelectAll.clicked.connect(self.select_all_lights)
        self.buttonDeselectAll.clicked.connect(self.deselect_all_lights)
        self.buttonSetSelection.clicked.connect(self.set_light_selection)
        self.buttonClearSelection.clicked.connect(self.clear_light_selection)
        #

        # Automatic Lights Control
        self.buttonResetDefaultTurnOnInstant.clicked.connect(self.reset_default_interval)
        self.buttonShuffleSequence.clicked.connect(self.shuffle_sequence)
        self.buttonShuffleInstants.clicked.connect(self.shuffle_instants)
        self.buttonSetManualAdjustments.clicked.connect(self.set_manual_adjustments)
        self.buttonSaveSequence.clicked.connect(self.save_sequence)
        self.buttonLoadSequence.clicked.connect(self.load_sequence)
        #

        # Test Control
        self.buttonOpenLightsWindow.clicked.connect(self.open_lights_window)
        self.buttonStartSession.clicked.connect(self.start_session)
        self.buttonStopSession.clicked.connect(self.stop_session)
        self.buttonSaveLogs.clicked.connect(self.save_logs)
        #

        """ Value change events """
        self.spinNumberBlocks.valueChanged.connect(self.change_number_of_blocks)

        for light in self.lightCheckBoxes:
            light.clicked.connect(self.manual_light_control)

        """ Tree selection event """
        self.treeLightSequence.currentItemChanged.connect(self.update_manual_adjust)

        """ Hotkey connections """
        self.shuffle_sequence_hotkey.activated.connect(self.shuffle_both)  # Shuffle all values: 'r'

        """ Signals """
        self.signal_on.signal.connect(lambda: self.turn_light_on(self.light_index))
        self.signal_off.signal.connect(lambda: self.turn_light_off(self.light_index))
        self.signal_countdown.signal.connect(self.update_countdown)
        self.signal_finished.signal.connect(self.stop_session)

    @staticmethod
    def message_box(msg_code, extra=None):
        """ Icon selection for message box """
        icon_information, icon_warning, icon_error, icon_question = 1, 2, 3, 4
        window_icon = "icons/logo.png"
        if msg_code == "no_lights":
            text = "No lights selected."
            icon = icon_warning
            title = "Light selection"
        elif msg_code == "file_save_error":
            text = "Error saving %s." % extra
            icon = icon_warning
            title = "File error"
        elif msg_code == "file_open_error":
            text = "Error opening %s.\nCheck file and try again." % extra
            icon = icon_warning
            title = "File error"
        elif msg_code == "file_saved":
            text = "%s saved successfully." % extra
            icon = icon_information
            title = "File saved"
        elif msg_code == "session_finished":
            text = "Session finished."
            icon = icon_information
            title = "Session finished"
        elif msg_code == "confirm_start":
            text = "Last session was not saved.\nAre you sure you want to start new session?"
            icon = icon_question
            title = "Last session not saved"
            window_icon = "icons/start.png"
        elif msg_code == "confirm_stop":
            text = "Are you sure you want to stop the current session?"
            icon = icon_question
            title = "Stop session"
            window_icon = "icons/stop.png"
        elif msg_code == "confirm_quit":
            text = "Are you sure you want to quit the application?"
            icon = icon_question
            title = "Quit"
            window_icon = "icons/clear.png"
        else:
            text = "Unknown error."
            icon = icon_error
            title = "Error"
        msg_box = QtWidgets.QMessageBox()
        if msg_code in ["confirm_start", "confirm_stop", "confirm_quit"]:
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            default_button = QtWidgets.QMessageBox.No
        else:
            default_button = QtWidgets.QMessageBox.Ok
        msg_box.setText(text)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setWindowIcon(QtGui.QIcon(window_icon))
        msg_box.setDefaultButton(default_button)
        return msg_box.exec_()

    @staticmethod
    def set_spin(spin, **kwargs):  # kws: value, min, max, increment
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
                self.enable_light(light_n)
            else:
                light.setDisabled(True)                         # Disable unchecked boxes
                self.disable_light(light_n)
        if self.selectedLights:                                 # Enable lights control
            self.buttonSetSelection.setDisabled(True)
            self.buttonSelectAll.setDisabled(True)
            self.buttonDeselectAll.setDisabled(True)
            self.buttonClearSelection.setEnabled(True)
            self.groupTestControl.setEnabled(True)
            self.groupLightsControl.setEnabled(True)

            self.create_sequence_tree()
        else:
            for light in self.lightCheckBoxes:                  # Enable all boxes if none were checked
                light.setEnabled(True)
            self.message_box("no_lights")                       # Warning message

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
        if not self.lightsWindow.is_open:         # If lights window isn't open, open it
            self.lightsWindow.open_maximized()
            self.turn_off_all_lights()            # Ensure all lights off
            self.buttonOpenLightsWindow.setText("    Close lights window")
            self.buttonStartSession.setEnabled(True)
            self.lightsWindow.is_open = True
        elif not self.on_session:                 # If lights window is open AND there isn't a ongoing session, close it
            self.lightsWindow.close()
            self.buttonOpenLightsWindow.setText("    Open lights window")
            self.buttonStartSession.setDisabled(True)
            self.lightsWindow.is_open = False

    def create_sequence_tree(self):
        """ Create the sequence list """
        self.treeLightSequence.clear()
        n_lights = self.spinNumberBlocks.value()
        default_interval = self.spinDefaultTurnOnInstant.value()
        light = iter(self.selectedLights)                     # Iterator used to add lights in the correct sequence
        if not self.treeLightSequence.topLevelItemCount():
            for light_n in range(n_lights):
                try:
                    c_light = next(light)
                except StopIteration:                         # Reset to first available light
                    light = iter(self.selectedLights)
                    c_light = next(light)
                finally:
                    # Build item and add to tree
                    tree_item = [str(light_n+1), str(c_light), str(default_interval)]
                    tree_item = QtWidgets.QTreeWidgetItem(tree_item)
                    self.align_tree_item(tree_item)
                    self.treeLightSequence.addTopLevelItem(tree_item)
            # Setting display to total session time
            self.lcdTotalTime.display(n_lights * self.spinBlockLength.value())

    def change_number_of_blocks(self):
        """ Copy tree items """
        tree_items = self.copy_tree()

        difference = self.spinNumberBlocks.value() - len(tree_items)
        selected_lights = list(self.selectedLights.keys())
        if difference > 0:                                                   # Number increased
            for new_light in range(difference):
                last_light_number = int(tree_items[-1][1])                   # Light number for last item in tree
                light_index = selected_lights.index(last_light_number) + 1   # Index for subsequent light
                if light_index >= len(selected_lights):                      # If index out of bounds, back to first
                    light_index = 0
                light_number = selected_lights[light_index]
                new_tree_item = [str(int(tree_items[-1][0]) + 1), str(light_number),
                                 str(self.spinDefaultTurnOnInstant.value())]
                tree_items.append(new_tree_item)

        elif difference < 0:  # Number decreased
            tree_items = tree_items[:difference]

        else:
            return

        """ Rebuild tree """
        self.build_tree(tree_items)

    def reset_default_interval(self):
        default_interval = self.spinDefaultTurnOnInstant.value()

        """ Copy and edit tree """
        tree_items = self.copy_tree()
        tree_items[:] = [[item[0], item[1], str(default_interval)] for item in tree_items]

        """ Rebuild tree """
        self.build_tree(tree_items)

    def shuffle_sequence(self):
        """ Copy tree items """
        tree_items = self.copy_tree()

        if tree_items:
            """ Create list with selected lights, then shuffle it """
            light_sequence = []
            for light_n in self.selectedLights.keys():
                light_sequence.append(light_n)
            shuffle(light_sequence)
            lights = iter(light_sequence)                           # Iterator for shuffled lights

            """ Distribute evenly between lights when randomizing """
            if self.checkEvenDist.isChecked():
                for light_n in range(self.spinNumberBlocks.value()):   # Iterating through lights
                    try:
                        light = next(lights)
                    except StopIteration:                        # Reshuffle and restart iteration for
                        shuffle(light_sequence)           # number of lights > available lights
                        lights = iter(light_sequence)
                        light = next(lights)
                    finally:
                        tree_items[light_n][1] = str(light)
            else:  # Distribution completely random
                for light_n in range(self.spinNumberBlocks.value()):
                    # Select one light at random from the available ones
                    tree_items[light_n][1] = str(choice(light_sequence))

            """ Rebuild lights tree """
            self.build_tree(tree_items)

    def shuffle_instants(self):
        """ Copy tree items """
        tree_items = self.copy_tree()

        if tree_items:
            """ Set possible intervals """
            min_interval = self.spinMinimumInstant.value()
            max_interval = self.spinMaximumInstant.value()
            possible_intervals = range(min_interval, max_interval + 1, 1)

            """ Pick from possible intervals """
            tree_items[:] = [[item[0], item[1], str(choice(possible_intervals))]
                             for item in tree_items]

            """ Rebuild lights tree """
            self.build_tree(tree_items)

    def shuffle_both(self):
        if self.groupLightsControl.isEnabled():
            self.shuffle_sequence()
            self.shuffle_instants()

    def update_manual_adjust(self):
        item_selected = self.treeLightSequence.currentItem()                        # Item selected on tree
        if item_selected:
            self.groupManualAdjusts.setEnabled(True)
            self.comboChangeLight.clear()
            for light in self.selectedLights.keys():                             # Adds available lights to combo box
                self.comboChangeLight.addItem(str(light))
            self.comboChangeLight.setCurrentText(item_selected.text(1))
            self.spinChangeTurnOnInstant.setValue(int(item_selected.text(2)))
        else:
            self.groupManualAdjusts.setDisabled(True)
            self.comboChangeLight.clear()

    def set_manual_adjustments(self):
        light_selection = str(self.comboChangeLight.currentText())       # New light that will be set
        instant_selection = str(self.spinChangeTurnOnInstant.value())    # New Turn ON Instant that will be set

        item_selected = self.treeLightSequence.currentItem()
        selected_index = int(item_selected.text(0)) - 1
        new_item = [item_selected.text(0), light_selection, instant_selection]
        new_item = QtWidgets.QTreeWidgetItem(new_item)
        self.align_tree_item(new_item)

        self.treeLightSequence.takeTopLevelItem(selected_index)                # Remove old item
        self.treeLightSequence.insertTopLevelItem(selected_index, new_item)    # Insert edited item
        self.treeLightSequence.setCurrentItem(self.treeLightSequence.topLevelItem(selected_index))

    def save_sequence(self):
        name = "ReactionTime_Sequence_%s" % datetime.datetime.now().strftime("%Y%m%d")
        name = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QFileDialog(), caption="Save current sequence",
                                                     directory=os.path.join(os.getcwd(), name),
                                                     filter="Text files (*.txt)",
                                                     options=QtWidgets.QFileDialog.DontConfirmOverwrite)
        if name[0]:
            name = name[0]
            # Add _2, _3... if name is repeated
            file_number = 2
            t_name = name
            while os.path.exists(t_name):
                t_name = name[:-4] + "_%d.txt" % file_number
                file_number += 1
            name = t_name
            tree_items = self.copy_tree()
            try:
                file = open(name, 'w')
                date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write("Sequence list for ReactionTime. Created on %s.\n" % date_time)
                file.write("[Block number]\t[Light Number]\t[Turn on at (s)]\n")
                for item in tree_items:
                    file.write("%s\t%s\t%.1f\n" % (item[0], item[1], float(item[2])))
                self.message_box("file_saved", os.path.split(name)[1])
            except EnvironmentError:
                self.message_box("file_save_error", os.path.split(name)[1])

    def load_sequence(self):
        name = QtWidgets.QFileDialog.getOpenFileName(QtWidgets.QFileDialog(), caption="Load sequence",
                                                     filter="Text file (*.txt)")
        if name[0]:
            name = name[0]
            try:
                file = open(name, 'r')
                tree_items = []
                data = file.readlines()
                while not data[0][0].isdigit():
                    data = data[1:]
                for line in data:
                    line = line.split()
                    tree_items.append(line)
                tree_items = [[item[0], item[1], item[2][:-2]] for item in tree_items]  # Remove decimal place from time
                self.build_tree(tree_items)
                self.spinNumberBlocks.setValue(self.treeLightSequence.topLevelItemCount())
            except Exception:  # Will be raised if any problems happen reading the file, including incompatible file
                self.message_box("file_open_error", os.path.split(name)[1])

    def start_session(self):
        if not self.last_session_saved:
            if self.message_box("confirm_start") == QtWidgets.QMessageBox.No:
                return
        if not self.autoLightControlThread.isRunning():
            self.turn_off_all_lights()
            self.terminate_thread = False
            self.on_session = True
            self.lightsWindow.can_close = False
            self.autoLightControlThread.start()  # Thread runs auto_light_control()
            self.start_datetime = str(datetime.datetime.now())
            self.textTestLogs.setText("Recording started at:\n%s\n" % self.start_datetime)
            self.session_toggle_widgets()
            self.buttonSaveLogs.setDisabled(True)

    def stop_session(self):
        if self.on_session:
            if self.message_box("confirm_stop") == QtWidgets.QMessageBox.No:
                return
        self.lightsWindow.can_close = True
        self.turn_off_all_lights()
        if self.autoLightControlThread.isRunning():
            self.lcdNextLight.display('0.0')
            self.lcdTimeRemaining.display('0.0')
            self.terminate_thread = True  # Stop thread
        self.session_toggle_widgets()
        self.buttonSaveLogs.setEnabled(True)
        self.last_session_saved = False
        if not self.on_session:
            self.message_box("session_finished")
        else:
            self.on_session = False

    def session_toggle_widgets(self):
        widgets = [self.buttonStopSession,
                   self.buttonStartSession,
                   self.groupLightsBorder,
                   self.groupLightsControl,
                   self.buttonOpenLightsWindow,
                   self.buttonClearSelection]
        for widget in widgets:
            widget.setDisabled(widget.isEnabled())

    def save_logs(self):
        name = "ReactionTime_RecordedSession%s" % datetime.datetime.now().strftime("%Y%m%d")
        name = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QFileDialog(), caption="Save last recording",
                                                     directory=os.path.join(os.getcwd(), name),
                                                     filter="Text files (*.txt)",
                                                     options=QtWidgets.QFileDialog.DontConfirmOverwrite)
        if name[0]:
            name = name[0]
            # Add _2, _3... if name is repeated
            file_number = 2
            t_name = name
            while os.path.exists(t_name):
                t_name = name[:-4] + "_%d.txt" % file_number
                file_number += 1
            name = t_name
            tree_items = self.copy_tree()
            try:
                file = open(name, 'w')
                file.write("ReactionTime session recorded on %s\n" % self.start_datetime)
                file.write("[Block number]\t[Light Number]\t[Switched on at (s)]\n")
                for item in tree_items:
                    file.write("%s\t%s\t%.1f\n" % (item[0], item[1], float(item[2])))
                self.message_box("file_saved", os.path.split(name)[1])
                self.last_session_saved = True
                log_file_name = name[:-4] + "_logs.txt"
                with open(log_file_name, 'w') as log_file:
                    log_file.writelines(self.textTestLogs.toPlainText())

            except EnvironmentError:
                self.message_box("file_save_error", os.path.split(name)[1])

    def manual_light_control(self):                                      # Connected when any checkbox is clicked
        if self.lightsWindow.is_open \
                and self.groupLightsBorder.isEnabled():                  # Only when lights window is open
            light_n = self.lightCheckBoxes.index(self.sender())          # Sender -> checkbox clicked
            for index in range(len(self.lightCheckBoxes)):
                if index != light_n:
                    self.turn_light_off(index)                           # Turn all other lights off/disable checkboxes
                else:
                    if self.sender().isChecked():                        # Turn correspondent light on if click is check
                        self.turn_light_on(index)
                    else:                                                # Turn off if click is uncheck
                        self.turn_light_off(index)

    def auto_light_control(self):
        tree_items = self.copy_tree()
        self.remaining_time = float(self.lcdTotalTime.intValue())
        if self.terminate_thread:
            return

        for item_index, item in enumerate(tree_items):
            self.current_in_sequence = item_index                     # Set current light in the sequence
            light_index, instant = int(item[1]), int(item[2])
            if item_index + 1 < len(tree_items):
                next_instant = int(tree_items[item_index+1][2])
            else:
                next_instant = 0

            self.time_until_next_light = instant
            time_on = self.spinDefaultOn.value()
            block_length = self.spinBlockLength.value()
            remaining_time = block_length - (instant + time_on)
            self.light_index = light_index - 1                        # Set light that will be controlled by the signals

            for i in range(instant * 10):                             # Wait 'instant' seconds before turning on
                self.signal_countdown.signal.emit()
                time.sleep(0.1)
                if self.terminate_thread:
                    return
            self.signal_on.signal.emit()                              # Turn on light

            if not next_instant:
                self.time_until_next_light = 0
            else:
                self.time_until_next_light = next_instant + time_on + remaining_time

            for i in range(time_on * 10):                             # Wait 'time_on' seconds before turning off
                self.signal_countdown.signal.emit()
                time.sleep(0.1)
                if self.terminate_thread:
                    self.signal_off.signal.emit()
                    return
            while self.lightCheckBoxes[self.light_index].isChecked():
                self.signal_off.signal.emit()                         # Turn off light

            for i in range(remaining_time * 10):                      # Wait for the remaining time of the block
                self.signal_countdown.signal.emit()
                time.sleep(0.1)
                if self.terminate_thread:
                    return

        self.signal_countdown.signal.emit()
        self.on_session = False
        self.signal_finished.signal.emit()

    def update_countdown(self):
        self.lcdTimeRemaining.display("%.1f" % float(self.remaining_time))
        self.lcdNextLight.display("%.1f" % float(self.time_until_next_light))
        self.remaining_time -= 0.1
        self.time_until_next_light -= 0.1
        if self.remaining_time < 0:
            self.remaining_time = 0
        if self.time_until_next_light < 0:
            self.time_until_next_light = 0

    def enable_light(self, light_index):
        self.lightCheckBoxes[light_index].setChecked(True)
        self.lightsWindow.enable_light(light_index)

    def disable_light(self, light_index):
        self.lightCheckBoxes[light_index].setChecked(False)
        self.lightsWindow.disable_light(light_index)

    def turn_light_on(self, light_index):
        self.lightCheckBoxes[light_index].setChecked(True)
        self.lightsWindow.turn_light_on(light_index)
        if self.on_session:
            self.textTestLogs.append("#%d> Light %d: %.1f" %
                                     (self.current_in_sequence + 1, light_index + 1,
                                      self.lcdTotalTime.intValue() - self.remaining_time))

    def turn_light_off(self, light_index):
        self.lightCheckBoxes[light_index].setChecked(False)
        self.lightsWindow.turn_light_off(light_index)

    def turn_off_all_lights(self):
        for light_index in range(len(self.lightsWindow.lights)):
            self.turn_light_off(light_index)

    def copy_tree(self):  # Copy items from tree and return list with them, members as strings
        tree_items = []
        for item_n in range(self.treeLightSequence.topLevelItemCount()):
            tree_item = self.treeLightSequence.topLevelItem(item_n)
            tree_item = [tree_item.text(0), tree_item.text(1), tree_item.text(2)]
            tree_items.append(tree_item)
        return tree_items

    def build_tree(self, tree_items):  # Build tree from items given in a list
        self.treeLightSequence.clear()
        for item in tree_items:
            item = QtWidgets.QTreeWidgetItem(item)
            self.align_tree_item(item)
            self.treeLightSequence.addTopLevelItem(item)
        self.treeLightSequence.scrollToBottom()
        self.lcdTotalTime.display(self.treeLightSequence.topLevelItemCount() * self.spinBlockLength.value())

    @staticmethod
    def align_tree_item(item):
        alignment = QtCore.Qt.AlignRight
        item.setTextAlignment(0, alignment)
        item.setTextAlignment(1, alignment)
        item.setTextAlignment(2, alignment)

    def closeEvent(self, event):
        event.ignore()
        if self.message_box("confirm_quit") == QtWidgets.QMessageBox.Yes:
            self.lightsWindow.can_close = True
            self.lightsWindow.close()
            event.accept()


class Thread(QtCore.QThread):
    def __init__(self, what_to_run):
        QtCore.QThread.__init__(self)
        self.what_to_run = what_to_run

    def __del__(self):
        self.wait()

    def run(self):
        self.what_to_run()


class Signal(QtWidgets.QWidget):
    signal = QtCore.pyqtSignal()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = ControlWindow()
    ui.show()
    sys.exit(app.exec_())
