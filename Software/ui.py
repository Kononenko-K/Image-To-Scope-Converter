#!/usr/bin/env python3
'''
===============================================================================
Filename: ui.py
-------------------------------------------------------------------------------
Created on: 2025-09-05

License:
    MIT License
    Copyright (c) 2023-2025 Kirill Kononenko
===============================================================================
'''
import darkdetect
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import cv2
import serial
from serial.tools import list_ports
import math
import sys


class ThemeManager:

    def __init__(self, app: QApplication):
        self.app = app
        self.is_dark = False

    def _apply_palette(self, palette: QPalette, disabled_color: QColor):
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text,
                         disabled_color)
        palette.setColor(QPalette.ColorGroup.Disabled,
                         QPalette.ColorRole.ButtonText, disabled_color)
        palette.setColor(QPalette.ColorGroup.Disabled,
                         QPalette.ColorRole.WindowText, disabled_color)
        palette.setColor(QPalette.ColorGroup.Disabled,
                         QPalette.ColorRole.HighlightedText, disabled_color)

        self.app.setPalette(palette)

    def set_dark_palette(self):
        self.app.setStyle('Fusion')
        dark_palette = QPalette()

        window_color = QColor(45, 45, 45)
        window_text_color = QColor(255, 255, 255)
        base_color = QColor(30, 30, 30)
        alternate_base_color = window_color
        tooltip_base_color = QColor(255, 255, 255)
        tooltip_text_color = QColor(255, 255, 255)
        text_color = QColor(255, 255, 255)
        button_color = window_color
        button_text_color = QColor(255, 255, 255)
        bright_text_color = QColor(255, 0, 0)
        link_color = QColor(42, 130, 218)
        highlight_color = QColor(42, 130, 218)
        highlighted_text_color = QColor(255, 255, 255)

        disabled_text_color = QColor(127, 127, 127)

        dark_palette.setColor(QPalette.ColorRole.Window, window_color)
        dark_palette.setColor(QPalette.ColorRole.WindowText,
                               window_text_color)
        dark_palette.setColor(QPalette.ColorRole.Base, base_color)
        dark_palette.setColor(QPalette.ColorRole.AlternateBase,
                              alternate_base_color)
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase,
                              tooltip_base_color)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText,
                              tooltip_text_color)
        dark_palette.setColor(QPalette.ColorRole.Text, text_color)
        dark_palette.setColor(QPalette.ColorRole.Button, button_color)
        dark_palette.setColor(QPalette.ColorRole.ButtonText,
                               button_text_color)
        dark_palette.setColor(QPalette.ColorRole.BrightText, bright_text_color)
        dark_palette.setColor(QPalette.ColorRole.Link, link_color)
        dark_palette.setColor(QPalette.ColorRole.Highlight, highlight_color)
        dark_palette.setColor(QPalette.ColorRole.HighlightedText,
                              highlighted_text_color)

        self._apply_palette(dark_palette, disabled_text_color)
        self.is_dark = True

    def set_light_palette(self):
        self.app.setStyle('Fusion')
        light_palette = QPalette()

        window_color = QColor(240, 240, 240)
        window_text_color = QColor(0, 0, 0)
        base_color = QColor(255, 255, 255)
        alternate_base_color = QColor(225, 225, 225)
        tooltip_base_color = QColor(255, 255, 220)
        tooltip_text_color = QColor(0, 0, 0)
        text_color = QColor(0, 0, 0)
        button_color = QColor(240, 240, 240)
        button_text_color = QColor(0, 0, 0)
        bright_text_color = QColor(255, 0, 0)
        link_color = QColor(0, 0, 255)
        highlight_color = QColor(0, 120, 215)
        highlighted_text_color = QColor(255, 255, 255)

        disabled_text_color = QColor(127, 127, 127)

        light_palette.setColor(QPalette.ColorRole.Window, window_color)
        light_palette.setColor(QPalette.ColorRole.WindowText,
                               window_text_color)
        light_palette.setColor(QPalette.ColorRole.Base, base_color)
        light_palette.setColor(QPalette.ColorRole.AlternateBase,
                               alternate_base_color)
        light_palette.setColor(QPalette.ColorRole.ToolTipBase,
                               tooltip_base_color)
        light_palette.setColor(QPalette.ColorRole.ToolTipText,
                               tooltip_text_color)
        light_palette.setColor(QPalette.ColorRole.Text, text_color)
        light_palette.setColor(QPalette.ColorRole.Button, button_color)
        light_palette.setColor(QPalette.ColorRole.ButtonText,
                               button_text_color)
        light_palette.setColor(QPalette.ColorRole.BrightText,
                               bright_text_color)
        light_palette.setColor(QPalette.ColorRole.Link, link_color)
        light_palette.setColor(QPalette.ColorRole.Highlight, highlight_color)
        light_palette.setColor(QPalette.ColorRole.HighlightedText,
                               highlighted_text_color)

        self._apply_palette(light_palette, disabled_text_color)
        self.is_dark = False


class Main(QWidget):
    outimg = [[135, 24], [67, 99]]

    def __init__(self):
        super(Main, self).__init__()
        self.resize(550, 420)
        self.setWindowIcon(QIcon('icon.ico'))
        self.label = QLabel(self)
        self.newAction = QAction(self)
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 550, 20))
        self.shadow = QGraphicsDropShadowEffect(self,
                                                blurRadius=7.5,
                                                color=QColor(40, 40, 40),
                                                offset=QPointF(0.5, 0.5))
        self.menuBar.setGraphicsEffect(self.shadow)
        self.openAction = QAction('Open', self)
        self.exitAction = QAction('Exit', self)
        self.setDarkAction = QAction('Dark', self)
        self.setLightAction = QAction('Light', self)
        self.fileMenu = QMenu('File', self)
        self.fileMenu_theme = QMenu('Theme', self)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addMenu(self.fileMenu_theme)
        self.fileMenu.addAction(self.exitAction)
        self.menuBar.addMenu(self.fileMenu)
        self.fileMenu_theme.addAction(self.setDarkAction)
        self.fileMenu_theme.addAction(self.setLightAction)
        self.exitAction.triggered.connect(self.close)
        self.label.setGeometry(QRect(143, 75, 270, 270))
        self.lineEdit = QLineEdit(u'lineEdit', self)
        self.lineEdit.setGeometry(QRect(20, 45, 431, 23))
        self.label_1 = QLabel(self)
        self.label_1.setObjectName(u'label_1')
        self.label_1.setGeometry(QRect(20, 130, 80, 16))
        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u'label_2')
        self.label_2.setGeometry(QRect(20, 340, 69, 16))
        self.label_3 = QLabel(self)
        self.label_3.setObjectName(u'label_3')
        self.label_3.setGeometry(QRect(430, 340, 125, 16))
        self.label_4 = QLabel(self)
        self.label_4.setObjectName(u'label_4')
        self.label_4.setGeometry(QRect(430, 160, 80, 16))
        self.res_line_comboBox = QComboBox(self)
        self.res_line_comboBox.setGeometry(QRect(20, 150, 85, 23))
        self.res_line_comboBox.addItems(
            ['64x64', '128x128', '256x256', '512x512', '1024x1024'])
        self.checkBox_invert = QCheckBox(self)
        self.checkBox_invert.setObjectName(u'checkBox')
        self.checkBox_invert.setGeometry(QRect(20, 180, 85, 23))
        self.pushButton = QPushButton(u'pushButton', self)
        self.pushButton.setGeometry(QRect(460, 45, 75, 23))
        self.pushButton_2 = QPushButton(u'pushButton_2', self)
        self.pushButton_2.setGeometry(QRect(240, 360, 75, 23))
        self.pushButton_refresh = QPushButton(u'pushButton_refresh', self)
        self.pushButton_refresh.setGeometry(QRect(430, 210, 100, 22))
        self.comboBox = QComboBox(self)
        self.comboBox.addItems([
            '9600', '38400', '57600', '115200', '250000', '500000', '1000000'
        ])
        self.comboBox.setGeometry(QRect(20, 360, 85, 22))
        self.uart_list_comboBox = QComboBox(self)
        self.uart_list_comboBox.setGeometry(QRect(430, 180, 100, 22))
        com_list = list_ports.comports()
        com_names = []
        for i in range(len(list_ports.comports())):
            com_names.append(list_ports.comports()[i].device)
        com_names.append('Test mode')
        self.uart_list_comboBox.addItems(com_names)
        self.algorithm_list_comboBox = QComboBox(self)
        self.algorithm_list_comboBox.setGeometry(QRect(430, 360, 100, 23))
        self.algorithm_list_comboBox.addItems(
            ['Global Thresholding', 'Adaptive Gaussian Thresholding'])
        self.frame = QFrame(self)
        self.frame.setObjectName(u'frame')
        self.frame.setGeometry(QRect(140, 70, 261, 261))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.pushButton.clicked.connect(self.showDialog)
        self.openAction.triggered.connect(self.showDialog)
        self.setDarkAction.triggered.connect(self.setDark)
        self.setLightAction.triggered.connect(self.setLight)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_refresh.clicked.connect(self.refresh)
        self.mouse_pressed = True

        self.res = 0
        self.density = 0
        self.ser = serial.Serial()
        self.im_show = []
        self.w_grid = 143
        self.h_grid = 75
        self.grid_arr = []
        self.im_show = []
        for i in range(256):
            for j in range(256):
                arr = []
                if ((i + 3) % 20) == 0 or ((j + 3) % 20) == 0:
                    arr.append(i)
                    arr.append(j)
                    self.grid_arr.append(arr)

        self.theme_manager = ThemeManager(app)
        if darkdetect.isDark():
            self.theme_manager.set_dark_palette()
            self.QPenColor = QPen(Qt.GlobalColor.darkGreen)
        else:
            self.theme_manager.set_light_palette()
            self.QPenColor = QPen(Qt.GlobalColor.red)

        self.retranslateUi()

        if len(sys.argv) > 1:
            self.lineEdit.setText(sys.argv[1])

    def retranslateUi(self):
        self.setWindowTitle(
            QCoreApplication.translate('MainWindow', u'Image to Scope', None))
        self.label_1.setText(
            QCoreApplication.translate('MainWindow', u'Resolution:', None))
        self.label_2.setText(
            QCoreApplication.translate('MainWindow', u'Baudrate:', None))
        self.label_3.setText(
            QCoreApplication.translate('MainWindow', u'Threshold:', None))
        self.label_4.setText(
            QCoreApplication.translate('MainWindow', u'COM ports:', None))
        self.lineEdit.setText(
            QCoreApplication.translate('MainWindow', u'Path to File', None))
        self.pushButton.setText(
            QCoreApplication.translate('MainWindow', u'Open', None))
        self.pushButton_2.setText(
            QCoreApplication.translate('MainWindow', u'Run', None))
        self.pushButton_refresh.setText(
            QCoreApplication.translate('MainWindow', u'Scan', None))
        self.checkBox_invert.setText(
            QCoreApplication.translate('Dialog', u'Invert', None))

    def setDark(self):
        self.theme_manager.set_dark_palette()
        self.QPenColor = QPen(Qt.GlobalColor.darkGreen)

    def setLight(self):
        self.theme_manager.set_light_palette()
        self.QPenColor = QPen(Qt.GlobalColor.red)

    def refresh(self):
        self.com_names = ['Test mode']
        for i in range(len(list_ports.comports())):
            self.com_names.append(list_ports.comports()[i].device)
        self.uart_list_comboBox.clear()
        self.uart_list_comboBox.addItems(self.com_names)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
        size = self.size()
        for i in range(len(self.grid_arr)):
            qp.drawPoint(self.grid_arr[i][0] + self.w_grid,
                         self.grid_arr[i][1] + self.h_grid)

        qp.setPen(self.QPenColor)
        size = self.size()
        for i in self.im_show:
            qp.drawPoint(i[0], i[1])
        self.update()
        QThread.msleep(10)

    def rotateImage(self, image, angleInDegrees):
        image = cv2.flip(image, 1)
        h, w = image.shape[:2]
        img_c = (w / 2, h / 2)

        rot = cv2.getRotationMatrix2D(img_c, angleInDegrees, 1)

        rad = math.radians(angleInDegrees)
        sin = math.sin(rad)
        cos = math.cos(rad)
        b_w = int((h * abs(sin)) + (w * abs(cos)))
        b_h = int((h * abs(cos)) + (w * abs(sin)))

        rot[0, 2] += ((b_w / 2) - img_c[0])
        rot[1, 2] += ((b_h / 2) - img_c[1])

        outImg = cv2.warpAffine(image, rot, (b_w, b_h), flags=cv2.INTER_LINEAR)
        return outImg

    def showDialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Path to Image')
        if fname:
            self.lineEdit.setText(fname)

    def im_process(self, im_in):
        try:
            im_in = cv2.cvtColor(im_in, cv2.COLOR_BGR2GRAY)
            h, w = im_in.shape[0:2]
            x = 0
            y = 0
            if (h > w):
                im_in = im_in[y:y + w, x:x + w]
            else:
                im_in = im_in[y:y + h, x:x + h]
            im_in = cv2.resize(im_in, (self.res, self.res))
            if self.algorithm_list_comboBox.currentText(
            ) == 'Global Thresholding':
                (thresh,
                 im_in) = cv2.threshold(im_in, 128, 255,
                                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            if self.algorithm_list_comboBox.currentText(
            ) == 'Adaptive Gaussian Thresholding':
                im_in = cv2.adaptiveThreshold(im_in, 255,
                                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY, 11, 2)
            im_show = cv2.resize(im_in, (256, 256))
            if self.checkBox_invert.checkState() == Qt.CheckState.Checked:
                print('is inverted')
                im_show = cv2.bitwise_not(im_show)
            else:
                print('is not inverted')
                im_in = cv2.bitwise_not(im_in)
            self.im_show = []
            for v in range(256):
                for h in range(256):
                    if im_show[v][h] == 0:
                        self.im_show.append([h + self.w_grid, v + self.h_grid])
            im_in = self.rotateImage(im_in, 180)
            return im_in
        except Exception as e:
            print(e)

    def uart_convert(self, cv2_im):
        cv2_im = self.im_process(cv2_im)
        im_arr = []
        for v in range(self.res):
            for h in range(self.res):
                if (h % 8 == 0):
                    im_arr.append(
                        bool(cv2_im[v][h]) * 1 + bool(cv2_im[v][h + 1]) * 2 +
                        bool(cv2_im[v][h + 2]) * 4 +
                        bool(cv2_im[v][h + 3]) * 8 +
                        bool(cv2_im[v][h + 4]) * 16 +
                        bool(cv2_im[v][h + 5]) * 32 +
                        bool(cv2_im[v][h + 6]) * 64 +
                        bool(cv2_im[v][h + 7]) * 128)
        return im_arr

    def run(self):
        try:
            self.res = int(self.res_line_comboBox.currentText().split('x')[0])
            im_in = cv2.imread(self.lineEdit.text())
            img_arr = self.uart_convert(im_in)

            if self.uart_list_comboBox.currentText() != 'Test mode':
                self.ser.baudrate = self.comboBox.currentText()
                self.ser.port = self.uart_list_comboBox.currentText()
                self.ser.open()
                im_b = bytearray(img_arr)
                self.ser.write(im_b)
                self.ser.close()
                print(len(im_b))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'{e}',
                                 QMessageBox.StandardButton.Ok)

    def openTargetFolder(self):
        folder_path = Path.parent(self.lineEdit.text())
        print(folder_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.setFixedSize(550, 420)
    ex.show()
    app.exec()
