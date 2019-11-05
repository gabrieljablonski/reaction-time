# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from RTFilesWindow import RTFilesWindow
import matplotlib
import numpy as np
import time
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.grid(linestyle='--')

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        return


def delsys_emg_channels(file_path):
    channels = {
        "T": [],
        "DA": [],
        "BB": [],
        "TB": [],
        "TG": []
    }
    try:
        with(open(file_path, 'r')) as file:
            for line in file.readlines()[285:]:
                line = line.replace(",", ".").split("\t")
                channels["T"].append(float(line[0]))
                channels["DA"].append(float(line[1]))
                channels["BB"].append(float(line[21]))
                channels["TB"].append(float(line[41]))
                channels["TG"].append(float(line[61]))

        for key, value in channels.items():
            if key != "T":
                channels[key] = np.array(value) / np.max(np.abs(value))

        return channels

    except Exception:
        return 0


class RTMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.loaded = False

        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.resize(1019, 508)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.chkMarker = QtWidgets.QCheckBox(self.centralWidget)
        self.chkMarker.setChecked(True)
        self.chkMarker.setObjectName("chkMarker")
        self.verticalLayout_5.addWidget(self.chkMarker)
        self.chkEMG = QtWidgets.QCheckBox(self.centralWidget)
        self.chkEMG.setChecked(True)
        self.chkEMG.setTristate(False)
        self.chkEMG.setObjectName("chkEMG")
        self.verticalLayout_5.addWidget(self.chkEMG)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.btnSave = QtWidgets.QPushButton(self.centralWidget)
        self.btnSave.setObjectName("btnSave")
        self.btnSave.clicked.connect(self.save_rts)
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.horizontalLayout_2.setStretch(1, 10)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabStage = QtWidgets.QTabWidget(self.centralWidget)
        self.tabStage.setObjectName("tabStage")
        self.tabStage.currentChanged.connect(self.plot)
        self.grid = QtWidgets.QWidget()
        self.grid.setObjectName("grid")
        self.gridLayout = QtWidgets.QGridLayout(self.grid)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tabPre = QtWidgets.QTabWidget(self.grid)
        self.tabPre.currentChanged.connect(self.plot)
        self.tabPre.setObjectName("tabPre")
        self.tabDA_pre = QtWidgets.QWidget()
        self.tabDA_pre.setObjectName("tabDA_pre")
        # self.gridTabDA_pre = QtWidgets.QGridLayout(self.tabDA_pre)
        # self.gridTabDA_pre.setContentsMargins(11, 11, 11, 11)
        # self.gridTabDA_pre.setSpacing(6)
        # self.gridTabDA_pre.setObjectName("gridLayout_6")
        self.tabPre.addTab(self.tabDA_pre, "")
        self.tabBB_pre = QtWidgets.QWidget()
        self.tabBB_pre.setObjectName("tabBB_pre")
        # self.gridTabBB_pre = QtWidgets.QGridLayout(self.tabBB_pre)
        # self.gridTabBB_pre.setContentsMargins(11, 11, 11, 11)
        # self.gridTabBB_pre.setSpacing(6)
        # self.gridTabBB_pre.setObjectName("gridLayout_7")
        self.tabPre.addTab(self.tabBB_pre, "")
        self.tabTB_pre = QtWidgets.QWidget()
        self.tabTB_pre.setObjectName("tabTB_pre")
        # self.gridTabTB_pre = QtWidgets.QGridLayout(self.tabTB_pre)
        # self.gridTabTB_pre.setContentsMargins(11, 11, 11, 11)
        # self.gridTabTB_pre.setSpacing(6)
        # self.gridTabTB_pre.setObjectName("gridLayout_8")
        self.tabPre.addTab(self.tabTB_pre, "")
        self.gridLayout.addWidget(self.tabPre, 0, 0, 1, 1)
        self.tabStage.addTab(self.grid, "")
        self.grid_2 = QtWidgets.QWidget()
        self.grid_2.setObjectName("grid_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.grid_2)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabPos = QtWidgets.QTabWidget(self.grid_2)
        self.tabPos.setObjectName("tabPos")
        self.tabPos.currentChanged.connect(self.plot)
        self.tabDA_pos = QtWidgets.QWidget()
        self.tabDA_pos.setObjectName("tabDA_pos")
        # self.gridTabDA_pos = QtWidgets.QGridLayout(self.tabDA_pos)
        # self.gridTabDA_pos.setContentsMargins(11, 11, 11, 11)
        # self.gridTabDA_pos.setSpacing(6)
        # self.gridTabDA_pos.setObjectName("gridLayout_9")
        self.tabPos.addTab(self.tabDA_pos, "")
        self.tabBB_pos = QtWidgets.QWidget()
        self.tabBB_pos.setObjectName("tabBB_pos")
        # self.gridTabBB_pos = QtWidgets.QGridLayout(self.tabBB_pos)
        # self.gridTabBB_pos.setContentsMargins(11, 11, 11, 11)
        # self.gridTabBB_pos.setSpacing(6)
        # self.gridTabBB_pos.setObjectName("gridLayout_10")
        self.tabPos.addTab(self.tabBB_pos, "")
        self.tabTB_pos = QtWidgets.QWidget()
        self.tabTB_pos.setObjectName("tabTB_pos")
        # self.gridTabTB_pos = QtWidgets.QGridLayout(self.tabTB_pos)
        # self.gridTabTB_pos.setContentsMargins(11, 11, 11, 11)
        # self.gridTabTB_pos.setSpacing(6)
        # self.gridTabTB_pos.setObjectName("gridLayout_11")
        self.tabPos.addTab(self.tabTB_pos, "")
        self.gridLayout_2.addWidget(self.tabPos, 0, 1, 1, 1)
        self.tabStage.addTab(self.grid_2, "")
        self.grid_3 = QtWidgets.QWidget()
        self.grid_3.setObjectName("grid_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.grid_3)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabRet = QtWidgets.QTabWidget(self.grid_3)
        self.tabRet.currentChanged.connect(self.plot)
        self.tabRet.setObjectName("tabRet")
        self.tabDA_ret = QtWidgets.QWidget()
        self.tabDA_ret.setObjectName("tabDA_ret")
        # self.gridTabDA_ret = QtWidgets.QGridLayout(self.tabDA_ret)
        # self.gridTabDA_ret.setContentsMargins(11, 11, 11, 11)
        # self.gridTabDA_ret.setSpacing(6)
        # self.gridTabDA_ret.setObjectName("gridLayout_12")
        self.tabRet.addTab(self.tabDA_ret, "")
        self.tabBB_ret = QtWidgets.QWidget()
        self.tabBB_ret.setObjectName("tabBB_ret")
        # self.gridTabBB_ret = QtWidgets.QGridLayout(self.tabBB_ret)
        # self.gridTabBB_ret.setContentsMargins(11, 11, 11, 11)
        # self.gridTabBB_ret.setSpacing(6)
        # self.gridTabBB_ret.setObjectName("gridLayout_13")
        self.tabRet.addTab(self.tabBB_ret, "")
        self.tabTB_ret = QtWidgets.QWidget()
        self.tabTB_ret.setObjectName("tabTB_ret")
        # self.gridTabTB_ret = QtWidgets.QGridLayout(self.tabTB_ret)
        # self.gridTabTB_ret.setContentsMargins(11, 11, 11, 11)
        # self.gridTabTB_ret.setSpacing(6)
        # self.gridTabTB_ret.setObjectName("gridLayout_14")
        self.tabRet.addTab(self.tabTB_ret, "")
        self.gridLayout_3.addWidget(self.tabRet, 0, 0, 1, 1)
        self.tabStage.addTab(self.grid_3, "")
        self.grid_4 = QtWidgets.QWidget()
        self.grid_4.setObjectName("grid_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.grid_4)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabPosOb = QtWidgets.QTabWidget(self.grid_4)
        self.tabPosOb.currentChanged.connect(self.plot)
        self.tabPosOb.setObjectName("tabPosOb")
        self.tabDA_posob = QtWidgets.QWidget()
        self.tabDA_posob.setObjectName("tabDA_posob")
        # self.gridTabDA_posob = QtWidgets.QGridLayout(self.tabDA_posob)
        # self.gridTabDA_posob.setContentsMargins(11, 11, 11, 11)
        # self.gridTabDA_posob.setSpacing(6)
        # self.gridTabDA_posob.setObjectName("gridLayout_15")
        self.tabPosOb.addTab(self.tabDA_posob, "")
        self.tabBB_posob = QtWidgets.QWidget()
        self.tabBB_posob.setObjectName("tabBB_posob")
        # self.gridTabBB_posob = QtWidgets.QGridLayout(self.tabBB_posob)
        # self.gridTabBB_posob.setContentsMargins(11, 11, 11, 11)
        # self.gridTabBB_posob.setSpacing(6)
        # self.gridTabBB_posob.setObjectName("gridLayout_17")
        self.tabPosOb.addTab(self.tabBB_posob, "")
        self.tabTB_posob = QtWidgets.QWidget()
        self.tabTB_posob.setObjectName("tabTB_posob")
        # self.gridTabTB_posob = QtWidgets.QGridLayout(self.tabTB_posob)
        # self.gridTabTB_posob.setContentsMargins(11, 11, 11, 11)
        # self.gridTabTB_posob.setSpacing(6)
        # self.gridTabTB_posob.setObjectName("gridLayout_16")
        self.tabPosOb.addTab(self.tabTB_posob, "")
        self.gridLayout_4.addWidget(self.tabPosOb, 0, 0, 1, 1)
        self.tabStage.addTab(self.grid_4, "")
        self.verticalLayout.addWidget(self.tabStage)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1019, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menuBar)
        self.actionOpenFiles = QtWidgets.QAction(self)
        self.actionOpenFiles.triggered.connect(self.open_files)
        self.actionOpenFiles.setObjectName("actionOpenFiles")
        self.actionQuit = QtWidgets.QAction(self)
        self.actionQuit.triggered.connect(self.close)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionOpenFiles)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.plotDA_pre = MyMplCanvas(self.tabDA_pre)
        self.plotBB_pre = MyMplCanvas(self.tabBB_pre)
        self.plotTB_pre = MyMplCanvas(self.tabTB_pre)

        self.plotDA_pos = MyMplCanvas(self.tabDA_pos)
        self.plotBB_pos = MyMplCanvas(self.tabBB_pos)
        self.plotTB_pos = MyMplCanvas(self.tabTB_pos)

        self.plotDA_ret = MyMplCanvas(self.tabDA_ret)
        self.plotBB_ret = MyMplCanvas(self.tabBB_ret)
        self.plotTB_ret = MyMplCanvas(self.tabTB_ret)

        self.plotDA_posob = MyMplCanvas(self.tabDA_posob)
        self.plotBB_posob = MyMplCanvas(self.tabBB_posob)
        self.plotTB_posob = MyMplCanvas(self.tabTB_posob)

        self.plot_figs = [[self.plotDA_pre, self.plotBB_pre, self.plotTB_pre],
                          [self.plotDA_pos, self.plotBB_pos, self.plotTB_pos],
                          [self.plotDA_ret, self.plotBB_ret, self.plotTB_ret],
                          [self.plotDA_posob, self.plotBB_posob, self.plotTB_posob]]

        self.picker = 2

        self.annotations = []

        self.emg_plot = None
        self.marker_plot = None
        self.reactions_plot = None
        self.stimuli_plot = None

        self.current_plot_fig = self.plot_figs[0][0]
        self.current_annotation = None

        for tab in self.plot_figs:
            for fig in tab:
                fig.fig.canvas.mpl_connect("motion_notify_event", self.hover)
                fig.fig.canvas.mpl_connect("pick_event", self.on_pick)

        l = QtWidgets.QVBoxLayout(self.tabDA_pre)
        l.addWidget(self.plotDA_pre)
        l.addWidget(NavigationToolbar(self.plotDA_pre, QtWidgets.QFrame(self.tabDA_pre)))
        l = QtWidgets.QVBoxLayout(self.tabBB_pre)
        l.addWidget(self.plotBB_pre)
        l.addWidget(NavigationToolbar(self.plotBB_pre, QtWidgets.QFrame(self.tabBB_pre)))
        l = QtWidgets.QVBoxLayout(self.tabTB_pre)
        l.addWidget(self.plotTB_pre)
        l.addWidget(NavigationToolbar(self.plotTB_pre, QtWidgets.QFrame(self.tabTB_pre)))

        l = QtWidgets.QVBoxLayout(self.tabDA_pos)
        l.addWidget(self.plotDA_pos)
        l.addWidget(NavigationToolbar(self.plotDA_pos, QtWidgets.QFrame(self.tabDA_pos)))
        l = QtWidgets.QVBoxLayout(self.tabBB_pos)
        l.addWidget(self.plotBB_pos)
        l.addWidget(NavigationToolbar(self.plotBB_pos, QtWidgets.QFrame(self.tabBB_pos)))
        l = QtWidgets.QVBoxLayout(self.tabTB_pos)
        l.addWidget(self.plotTB_pos)
        l.addWidget(NavigationToolbar(self.plotTB_pos, QtWidgets.QFrame(self.tabTB_pos)))

        l = QtWidgets.QVBoxLayout(self.tabDA_ret)
        l.addWidget(self.plotDA_ret)
        l.addWidget(NavigationToolbar(self.plotDA_ret, QtWidgets.QFrame(self.tabDA_ret)))
        l = QtWidgets.QVBoxLayout(self.tabBB_ret)
        l.addWidget(self.plotBB_ret)
        l.addWidget(NavigationToolbar(self.plotBB_ret, QtWidgets.QFrame(self.tabBB_ret)))
        l = QtWidgets.QVBoxLayout(self.tabTB_ret)
        l.addWidget(self.plotTB_ret)
        l.addWidget(NavigationToolbar(self.plotTB_ret, QtWidgets.QFrame(self.tabTB_ret)))

        l = QtWidgets.QVBoxLayout(self.tabDA_posob)
        l.addWidget(self.plotDA_posob)
        l.addWidget(NavigationToolbar(self.plotDA_posob, QtWidgets.QFrame(self.tabDA_posob)))
        l = QtWidgets.QVBoxLayout(self.tabBB_posob)
        l.addWidget(self.plotBB_posob)
        l.addWidget(NavigationToolbar(self.plotBB_posob, QtWidgets.QFrame(self.tabBB_posob)))
        l = QtWidgets.QVBoxLayout(self.tabTB_posob)
        l.addWidget(self.plotTB_posob)
        l.addWidget(NavigationToolbar(self.plotTB_posob, QtWidgets.QFrame(self.tabTB_posob)))

        self.channels = {
            "pre": {},
            "pos": {},
            "ret": {},
            "posob": {}
        }

        self.reactions = [[[], [], []],
                          [[], [], []],
                          [[], [], []],
                          [[], [], []]]
        self.stimuli = [[],
                        [],
                        [],
                        []]

        self.rts = [
            [[0]*5, [0]*5, [0]*5],
            [[0]*5, [0]*5, [0]*5],
            [[0]*5, [0]*5, [0]*5],
            [[0]*5, [0]*5, [0]*5]
        ]

        self.index_out = 0
        self.index_in = 0

        self.chkEMG.stateChanged.connect(self.toggle_visibility)
        self.chkMarker.stateChanged.connect(self.toggle_visibility)

        self.tabs = [self.tabPre, self.tabPos, self.tabRet, self.tabPosOb]

        QtWidgets.QShortcut("m", self).activated.connect(self.alternate_marker)
        QtWidgets.QShortcut("e", self).activated.connect(self.alternate_emg)

        self.retranslateUi()

        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Reaction Time Analysis"))
        self.chkMarker.setText(_translate("MainWindow", "Mostrar marcador"))
        self.chkEMG.setText(_translate("MainWindow", "Mostrar sinal de EMG"))
        self.btnSave.setText(_translate("MainWindow", "Salvar tempos de reação"))
        self.tabPre.setTabText(self.tabPre.indexOf(self.tabDA_pre), _translate("MainWindow", "Deltóide"))
        self.tabPre.setTabText(self.tabPre.indexOf(self.tabBB_pre), _translate("MainWindow", "Bíceps"))
        self.tabPre.setTabText(self.tabPre.indexOf(self.tabTB_pre), _translate("MainWindow", "Tríceps"))
        self.tabStage.setTabText(self.tabStage.indexOf(self.grid), _translate("MainWindow", "Pré"))
        self.tabPos.setTabText(self.tabPos.indexOf(self.tabDA_pos), _translate("MainWindow", "Deltóide"))
        self.tabPos.setTabText(self.tabPos.indexOf(self.tabBB_pos), _translate("MainWindow", "Bíceps"))
        self.tabPos.setTabText(self.tabPos.indexOf(self.tabTB_pos), _translate("MainWindow", "Tríceps"))
        self.tabStage.setTabText(self.tabStage.indexOf(self.grid_2), _translate("MainWindow", "Pós"))
        self.tabRet.setTabText(self.tabRet.indexOf(self.tabDA_ret), _translate("MainWindow", "Deltóide"))
        self.tabRet.setTabText(self.tabRet.indexOf(self.tabBB_ret), _translate("MainWindow", "Bíceps"))
        self.tabRet.setTabText(self.tabRet.indexOf(self.tabTB_ret), _translate("MainWindow", "Tríceps"))
        self.tabStage.setTabText(self.tabStage.indexOf(self.grid_3), _translate("MainWindow", "Retenção"))
        self.tabPosOb.setTabText(self.tabPosOb.indexOf(self.tabDA_posob), _translate("MainWindow", "Deltóide"))
        self.tabPosOb.setTabText(self.tabPosOb.indexOf(self.tabBB_posob), _translate("MainWindow", "Bíceps"))
        self.tabPosOb.setTabText(self.tabPosOb.indexOf(self.tabTB_posob), _translate("MainWindow", "Tríceps"))
        self.tabStage.setTabText(self.tabStage.indexOf(self.grid_4), _translate("MainWindow", "Pós-observação"))
        self.menuFile.setTitle(_translate("MainWindow", "&Arquivo"))
        self.actionOpenFiles.setText(_translate("MainWindow", "&Abrir arquivos"))
        self.actionQuit.setText(_translate("MainWindow", "&Sair"))

    def alternate_emg(self):
        self.chkEMG.setChecked(not self.chkEMG.isChecked())

    def alternate_marker(self):
        self.chkMarker.setChecked(not self.chkMarker.isChecked())

    def open_files(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QFileDialog(), caption="Load Files",
                                                       filter="Text files (*.txt)")
        if files[0]:
            files_window = RTFilesWindow(files[0])
            files_window.exec_()
            self.load_files(files_window.files)
            # self.plot()

    def load_files(self, files):
        for key in self.channels.keys():
            self.channels[key] = {}
        if files["pre"]:
            self.channels["pre"] = delsys_emg_channels(files["pre"])
        if files["pos"]:
            self.channels["pos"] = delsys_emg_channels(files["pos"])
        if files["ret"]:
            self.channels["ret"] = delsys_emg_channels(files["ret"])
        if files["posob"]:
            self.channels["posob"] = delsys_emg_channels(files["posob"])
        self.loaded = True
        self.rts = [
            [[0] * 5, [0] * 5, [0] * 5],
            [[0] * 5, [0] * 5, [0] * 5],
            [[0] * 5, [0] * 5, [0] * 5],
            [[0] * 5, [0] * 5, [0] * 5]
        ]
        self.reactions = [[[], [], []],
                          [[], [], []],
                          [[], [], []],
                          [[], [], []]]
        self.stimuli = [[],
                        [],
                        [],
                        []]
        self.plot()

    def update_annot(self, which, ind):
        if which == 'emg':
            x, y = self.emg_plot.get_data()
        elif which == 'marker':
            x, y = self.marker_plot.get_data()

        x = x[ind["ind"][0]]
        y = y[ind["ind"][0]]

        self.current_annotation.xy = (x, y)
        text = str(x) + " segundos"
        self.current_annotation.set_text(text)
        self.current_annotation.set_visible(True)

    def hover(self, event):
        if self.marker_plot and self.emg_plot:
            if event.inaxes == self.current_plot_fig.axes:
                cont, ind = self.marker_plot.contains(event)
                if cont:
                    self.update_annot('marker', ind)
                else:
                    cont, ind = self.emg_plot.contains(event)
                    if cont:
                        self.update_annot('emg', ind)
                    elif self.current_annotation.get_visible():
                        self.current_annotation.set_visible(False)
                self.redraw()

    def closest(self, which, point):
        if which == "emg":
            ref = self.reactions[self.index_out][self.index_in]
        else:
            ref = self.stimuli[self.index_out]
        min_d = (9999999, -1)
        for index, p in enumerate(ref):
            d = abs(point[0] - p[0])
            if d < min_d[0]:
                min_d = d, index
        return min_d[1]

    def on_pick(self, event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind

            r = self.reactions[self.index_out][self.index_in]
            s = self.stimuli[self.index_out]

            x = np.take(xdata, ind)[0]
            y = np.take(ydata, ind)[0]

            from operator import itemgetter

            if event.artist == self.emg_plot:
                if (x, y) in r:
                    r.remove((x, y))
                else:
                    if len(r) > 4:
                        r.pop(self.closest("emg", (x, y)))
                    r.append((x, y))
                    r.sort(key=itemgetter(0))
            elif event.artist == self.marker_plot:
                if (x, y) in s:
                    s.remove((x, y))
                else:
                    if len(s) > 4:
                        s.pop(self.closest("marker", (x, y)))
                    s.append((x, y))
                    s.sort(key=itemgetter(0))
            self.update_rt_plot()

    def plot(self):
        if self.loaded:
            self.clear_plots()

            emg_color = "black"
            emg_linestyle = "None"
            emg_linewidth = 1
            emg_marker = "o"
            emg_mfc = "blue"
            emg_markersize = 4

            trigger_color = "red"
            trigger_linestyle = "--"
            trigger_linewidth = 1
            trigger_marker = "o"
            trigger_mfc = "red"
            trigger_markersize = 3
            alpha = 0.6

            picker = self.picker

            self.index_out = self.tabStage.currentIndex()
            current_tab = self.tabs[self.index_out]

            self.index_in = current_tab.currentIndex()

            self.current_plot_fig = self.plot_figs[self.index_out][self.index_in]
            self.current_annotation = self.annotations[self.index_out][self.index_in]

            channels = []

            if self.index_out == 0:
                channels = self.channels["pre"]
            elif self.index_out == 1:
                channels = self.channels["pos"]
            elif self.index_out == 2:
                channels = self.channels["ret"]
            elif self.index_out == 3:
                channels = self.channels["posob"]

            ch = ""

            if self.index_in == 0:
                ch = "DA"
            elif self.index_in == 1:
                ch = "BB"
            elif self.index_in == 2:
                ch = "TB"

            if channels:
                p = self.plot_figs[self.index_out][self.index_in]

                self.marker_plot = p.axes.plot(channels["T"], channels["TG"], picker=picker,
                                                                              color=trigger_color,
                                                                              linestyle=trigger_linestyle,
                                                                              linewidth=trigger_linewidth,
                                                                              marker=trigger_marker, mfc=trigger_mfc,
                                                                              markersize=trigger_markersize,
                                                                              mec=trigger_mfc, alpha=alpha)[0]
                self.emg_plot = p.axes.plot(channels["T"], channels[ch], picker=picker,
                                              color=emg_color, linestyle=emg_linestyle, linewidth=emg_linewidth,
                                              marker=emg_marker, mfc=emg_mfc, markersize=emg_markersize)[0]
                self.reactions_plot = p.axes.plot([], [], linestyle="None", marker="X", mfc="green", mec="black",
                                                  markersize=10)[0]
                self.stimuli_plot = p.axes.plot([], [], linestyle="None", marker="X", mfc="pink", mec="black",
                                                markersize=10)[0]

                self.update_rt_plot()
                self.toggle_visibility()

    def update_rt_plot(self):
        r = self.reactions[self.index_out][self.index_in]
        s = self.stimuli[self.index_out]

        r_xs = np.array([point[0] for point in r])
        r_ys = [point[1] for point in r]

        s_xs = np.array([point[0] for point in s])
        s_ys = [point[1] for point in s]

        if r_xs.size <= s_xs.size:
            for index, x in enumerate(r_xs):
                self.rts[self.index_out][self.index_in][index] = x - s_xs[index]
        else:
            for index, x in enumerate(s_xs):
                self.rts[self.index_out][self.index_in][index] = r_xs[index] - x

        rts = self.rts[self.index_out][self.index_in]

        self.reactions_plot.set_data(r_xs, r_ys)
        self.stimuli_plot.set_data(s_xs, s_ys)

        self.current_plot_fig.axes.legend([self.reactions_plot], ["1º tempo de reação: %.4f\n" % (rts[0] if rts[0] else 0) +
                                           "2º tempo de reação: %.4f\n" % (rts[1] if rts[1] else 0) +
                                           "3º tempo de reação: %.4f\n" % (rts[2] if rts[2] else 0) +
                                           "4º tempo de reação: %.4f\n" % (rts[3] if rts[3] else 0) +
                                           "5º tempo de reação: %.4f\n" % (rts[4] if rts[4] else 0)], loc=1)

    def toggle_visibility(self):
        plot_marker = self.chkMarker.isChecked()
        plot_emg = self.chkEMG.isChecked()

        if self.emg_plot is not None:
            self.emg_plot.set_visible(plot_emg)
            self.reactions_plot.set_visible(plot_emg)
            if self.emg_plot.get_visible():
                self.emg_plot.set(picker=self.picker)
            else:
                self.emg_plot.set(picker=0)

        if self.marker_plot is not None:
            self.marker_plot.set_visible(plot_marker)
            self.stimuli_plot.set_visible(plot_marker)
            if self.marker_plot.get_visible():
                self.marker_plot.set(picker=self.picker)
            else:
                self.marker_plot.set(picker=0)

        self.redraw()

    def clear_plots(self):
        for stage in self.plot_figs:
            for plot in stage:
                plot.axes.clear()
                plot.axes.grid(linestyle='--')
        self.annotations = [[plot.axes.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                                bbox=dict(boxstyle="round", fc="w"),
                                                arrowprops=dict(arrowstyle="->")) for plot in plots] for plots in
                            self.plot_figs]
        for stage in self.annotations:
            for annot in stage:
                annot.set_visible(False)
        self.emg_plot = None
        self.marker_plot = None
        self.reactions_plot = None
        self.stimuli_plot = None

    def redraw(self):
        self.current_plot_fig.fig.canvas.draw_idle()

    def save_rts(self):
        file_name = QtWidgets.QFileDialog.getSaveFileName(QtWidgets.QFileDialog(), caption="Salvar tempos de reação",
                                                     filter="Text files (*.txt)")

        if file_name[0]:
            try:
                with open(file_name[0], 'w') as file:
                    file.write("\tPre\tPos\tRetencao\tPosObservacao\n")

                    file.write("Deltoide\t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][0][0], self.rts[1][0][0], self.rts[2][0][0], self.rts[3][0][0]))
                    file.write("        \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][0][1], self.rts[1][0][1], self.rts[2][0][1], self.rts[3][0][1]))
                    file.write("        \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][0][2], self.rts[1][0][2], self.rts[2][0][2], self.rts[3][0][2]))
                    file.write("        \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][0][3], self.rts[1][0][3], self.rts[2][0][3], self.rts[3][0][3]))
                    file.write("        \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][0][4], self.rts[1][0][4], self.rts[2][0][4], self.rts[3][0][4]))

                    file.write("\n\n")

                    file.write("Biceps\t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][1][0], self.rts[1][1][0], self.rts[2][1][0], self.rts[3][1][0]))
                    file.write("      \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][1][1], self.rts[1][1][1], self.rts[2][1][1], self.rts[3][1][1]))
                    file.write("      \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][1][2], self.rts[1][1][2], self.rts[2][1][2], self.rts[3][1][2]))
                    file.write("      \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][1][3], self.rts[1][1][3], self.rts[2][1][3], self.rts[3][1][3]))
                    file.write("      \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][1][4], self.rts[1][1][4], self.rts[2][1][4], self.rts[3][1][4]))

                    file.write("\n\n")

                    file.write("Triceps\t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][2][0], self.rts[1][2][0], self.rts[2][2][0], self.rts[3][2][0]))
                    file.write("       \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][2][1], self.rts[1][2][1], self.rts[2][2][1], self.rts[3][2][1]))
                    file.write("       \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][2][2], self.rts[1][2][2], self.rts[2][2][2], self.rts[3][2][2]))
                    file.write("       \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][2][3], self.rts[1][2][3], self.rts[2][2][3], self.rts[3][2][3]))
                    file.write("       \t%.4f\t%.4f\t%.4f\t%.4f\n" % (self.rts[0][2][4], self.rts[1][2][4], self.rts[2][2][4], self.rts[3][2][4]))

                msgbox = QtWidgets.QMessageBox()
                msgbox.setWindowTitle("Salvo")
                msgbox.setText("Tempos de reação salvos com sucesso")
                msgbox.setIcon(QtWidgets.QMessageBox.Information)
                msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgbox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                msgbox.exec_()

            except Exception:
                msgbox = QtWidgets.QMessageBox()
                msgbox.setWindowTitle("Erro")
                msgbox.setText("Erro ao salvar arquivo")
                msgbox.setIcon(QtWidgets.QMessageBox.Critical)
                msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgbox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                msgbox.exec_()

    def closeEvent(self, event):
        event.ignore()

        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Sair")
        msgbox.setText("Salvar antes de sair?")
        msgbox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.Save)

        option = msgbox.exec_()
        if option == QtWidgets.QMessageBox.Cancel:
            return
        elif option == QtWidgets.QMessageBox.Save:
            self.save_rts()
            event.accept()
        else:
            event.accept()


class Signal(QtWidgets.QWidget):
    signal = QtCore.pyqtSignal()


class NavigationToolbar(NavigationToolbar2QT):
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save', 'Back', 'Forward')]


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = RTMainWindow()
    ui.show()
    sys.exit(app.exec_())

