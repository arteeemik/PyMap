"""
The file is converted from pymap/ui/qt_basic_ui/welcome_page.ui to python.
Defines basic ui structure.
"""
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(794, 518)

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setObjectName("grid_layout")

        self.name_layout = QtWidgets.QGridLayout()
        self.name_layout.setObjectName("name_layout")
        self.name_line = QtWidgets.QFrame(self.central_widget)
        self.name_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.name_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.name_line.setObjectName("name_line")
        self.name_layout.addWidget(self.name_line, 1, 0, 1, 1)
        self.name_label = QtWidgets.QLabel(self.central_widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(32)
        self.name_label.setFont(font)
        self.name_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name_label.setAutoFillBackground(False)
        self.name_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.name_label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.name_label.setLineWidth(1)
        self.name_label.setTextFormat(QtCore.Qt.RichText)
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setWordWrap(False)
        self.name_label.setObjectName("nameLabel")
        self.name_layout.addWidget(self.name_label, 0, 0, 1, 1)
        self.grid_layout.addLayout(self.name_layout, 0, 0, 1, 1)

        self.city_layout = QtWidgets.QHBoxLayout()
        self.city_layout.setObjectName("city_layout")
        self.city_label = QtWidgets.QLabel(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.city_label.sizePolicy().hasHeightForWidth()
        )
        self.city_label.setSizePolicy(size_policy)
        self.city_label.setMinimumSize(QtCore.QSize(98, 0))
        self.city_label.setObjectName("city_label")
        self.city_layout.addWidget(self.city_label)
        self.city_line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.city_line_edit.setObjectName("city_line_edit")
        self.city_layout.addWidget(self.city_line_edit)
        self.grid_layout.addLayout(self.city_layout, 1, 0, 1, 1)

        self.address_area = QtWidgets.QScrollArea(self.central_widget)
        self.address_area.setWidgetResizable(True)
        self.address_area.setObjectName("address_area")
        self.address_area_contents = QtWidgets.QWidget()
        self.address_area_contents.setGeometry(QtCore.QRect(0, 0, 667, 90))
        self.address_area_contents.setObjectName("address_area_contents")
        self.address_grid_layout = QtWidgets.QGridLayout(
            self.address_area_contents
        )
        self.address_grid_layout.setObjectName("address_grid_layout")

        self.address_area.setWidget(self.address_area_contents)
        self.grid_layout.addWidget(self.address_area, 2, 0, 1, 1)

        self.buttons_grid_layout = QtWidgets.QGridLayout()
        self.buttons_grid_layout.setObjectName("buttons_grid_layout")
        self.new_address_push_button = QtWidgets.QPushButton(
            self.central_widget
        )
        self.new_address_push_button.setObjectName("new_address_push_button")
        self.buttons_grid_layout.addWidget(
            self.new_address_push_button, 0, 0, 1, 1
        )
        spacer_item1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.buttons_grid_layout.addItem(spacer_item1, 0, 1, 1, 1)
        self.get_route_push_button = QtWidgets.QPushButton(self.central_widget)
        self.get_route_push_button.setObjectName("get_route_push_button")
        self.buttons_grid_layout.addWidget(
            self.get_route_push_button, 0, 2, 1, 1
        )
        self.grid_layout.addLayout(self.buttons_grid_layout, 3, 0, 1, 1)
        main_window.setCentralWidget(self.central_widget)

        self.retranslate_ui(main_window)

        self.new_address_push_button.hide()

        self.city_line_edit.editingFinished.connect(
            self.new_address_push_button.show
        )

        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(
            _translate("main_window", "DiscoverYourCity")
        )
        self.name_label.setText(
            _translate("main_window", "Давайте построим маршрут экскурсии")
        )
        self.city_label.setText(_translate("main_window", "Введите город:"))
        self.get_route_push_button.setText(
            _translate("main_window", "Построить маршрут")
        )
        self.new_address_push_button.setText(
            _translate("main_window", "Добавить адрес")
        )
