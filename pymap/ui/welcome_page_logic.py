"""This file implements the welcome_page ui logic."""
from PyQt5 import QtWidgets

from .basic_ui.welcome_page import Ui_MainWindow


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Класс окна UI, определяет логику указания точек маршрута.

    Attributes
    --------
    address_number : int
    active_addresses : typing.Set[int]
    """

    FAILURE = -1
    SUCCESS = 0

    def __init__(self, parent: QtWidgets.QWidget = None):
        """
        Инициализация класса окна приложения.

        Parameters
        ---------
        parent : QtWidgets.QWidget
        """
        super().__init__(parent)
        self.setup_ui(self)
        self.lang = "ru"
        self.address_number = 0
        self.active_addresses = set()
        self.set_basic_slots()

    def set_basic_slots(self) -> None:
        """Связывает слоты изменения названия города с полями для адресов."""
        self.city_line_edit.textChanged.connect(self.clear_addresses)
        self.city_line_edit.editingFinished.connect(
            self.new_address_push_button.show
        )
        self.city_line_edit.editingFinished.connect(self.set_basic_address_view)
        self.new_address_push_button.clicked.connect(self.add_address)
        self.get_route_push_button.clicked.connect(self.get_route)
        self.comboBox.currentIndexChanged.connect(self.localization_change_func)

    def localization_change_func(self, index):
        """Переводит интерфейс на соответствующий язык."""
        self.lang = self.comboBox.itemData(index)
        for i in self.active_addresses:
            label = f"address_{i}_label"
            del_button = f"delete_address_{i}"
            self.__getattribute__(label).setText(
                self.labels_names["address_label"][self.lang]
            )
            self.__getattribute__(del_button).setText(
                self.labels_names["delete_address"][self.lang]
            )

    def get_route(self) -> None:
        """
        Реализует действия по нажатию кнопки "Построить маршрут".

        Собирает введенные данные в поля адресов.
        Передаёт их в построение маршрута.
        Переключает на окно отрисовки карты.
        """

        def _check_correctness() -> bool:
            is_ok = True
            for i in list(self.active_addresses):
                line_edit = f"address_{i}_line_edit"
                if self.__getattribute__(line_edit).text() == "":
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle(
                        self.labels_names["route_error_title"][self.lang]
                    )
                    msg.setText(self.labels_names["route_error_msg"][self.lang])
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setStandardButtons(
                        QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes
                    )
                    msg.setDefaultButton(QtWidgets.QMessageBox.Yes)

                    def _buttons_logic(code: int) -> None:
                        nonlocal is_ok
                        if code.text() == "&Yes":
                            ret = self.clear_empty_addresses()
                            is_ok = ret == 0
                        else:
                            is_ok = False

                    msg.buttonClicked.connect(_buttons_logic)

                    msg.exec_()
            return is_ok

        if not _check_correctness():
            return

        query = (
            self.city_line_edit.text(),
            [
                self.__getattribute__(f"address_{i}_line_edit").text()
                for i in self.active_addresses
            ],
        )
        # TODO: call function to create the route
        # TODO: call function to draw a map with the route
        # TODO: implement map drawing screen
        print(query)

    def clear_empty_addresses(self) -> int:
        """Убирает пустые строки адресов."""
        for i in list(self.active_addresses):
            line_edit = f"address_{i}_line_edit"
            if self.__getattribute__(line_edit).text() == "":
                ret = self.del_address(i)
                if ret == Window.FAILURE:
                    return ret
        return Window.SUCCESS

    def set_basic_address_view(self) -> None:
        """Удаляет все адреса и создаёт одну пустую ячейку для точки старта."""
        self.clear_addresses()
        self.add_address()

    def clear_addresses(self) -> None:
        """Удаляет все адреса из маршрута."""
        for i in self.active_addresses:
            self.hide_address(i)
        self.active_addresses.clear()

    def add_address(self) -> None:
        """Добавляет ячейку для очередной точки маршрута."""
        self.address_number += 1
        layout = f"address_{self.address_number}_layout"
        label = f"address_{self.address_number}_label"
        line_edit = f"address_{self.address_number}_line_edit"
        del_button = f"delete_address_{self.address_number}"
        self.__setattr__(layout, QtWidgets.QHBoxLayout())
        self.__getattribute__(layout).setObjectName(layout)
        self.__setattr__(label, QtWidgets.QLabel(self.address_area_contents))

        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.__getattribute__(label).sizePolicy().hasHeightForWidth()
        )

        self.__getattribute__(label).setSizePolicy(size_policy)
        self.__getattribute__(label).setObjectName(label)
        self.__getattribute__(layout).addWidget(self.__getattribute__(label))

        self.__setattr__(
            line_edit, QtWidgets.QLineEdit(self.address_area_contents)
        )
        self.__getattribute__(line_edit).setObjectName(line_edit)
        self.__getattribute__(layout).addWidget(
            self.__getattribute__(line_edit)
        )

        self.__setattr__(
            del_button, QtWidgets.QPushButton(self.address_area_contents)
        )
        self.__getattribute__(del_button).setObjectName(del_button)
        self.__getattribute__(layout).addWidget(
            self.__getattribute__(del_button)
        )

        self.address_grid_layout.addLayout(
            self.__getattribute__(layout), self.address_number, 0, 1, 1
        )
        self.__getattribute__(label).setText(
            self.labels_names["address_label"][self.lang]
        )
        self.__getattribute__(del_button).setText(
            self.labels_names["delete_address"][self.lang]
        )
        self.__getattribute__(del_button).clicked.connect(
            lambda state, x=self.address_number: self.del_address(x)
        )

        self.active_addresses.add(self.address_number)

    def del_address(self, curr_address_id: int) -> int:
        """
        Удаляет точку маршрута.

        Parameters
        ---------
        curr_address_id : int
            id ячейки адреса для удаления.
            example: 1
        Returns
        ---------
        exit_status : int
           успех удаления точки (в маршруте должна остаться хотя бы одна точка).
        """
        if len(self.active_addresses) == 1:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle(
                self.labels_names["single_address_error_title"][self.lang]
            )
            msg.setText(
                self.labels_names["single_address_error_msg"][self.lang]
            )
            msg.setIcon(QtWidgets.QMessageBox.Warning)

            msg.exec_()
            return Window.FAILURE

        self.hide_address(curr_address_id)

        self.active_addresses.discard(curr_address_id)
        return Window.SUCCESS

    def hide_address(self, address_id: int) -> None:
        """
        Прячет из интерфейса точку маршрута.

        Parameters
        ---------
        address_id : int
            id ячейки адреса для удаления из UI.
            example: 1
        """
        layout = f"address_{address_id}_layout"
        label = f"address_{address_id}_label"
        line_edit = f"address_{address_id}_line_edit"
        del_button = f"delete_address_{address_id}"
        self.__getattribute__(layout).setParent(None)
        self.__getattribute__(label).hide()
        self.__getattribute__(line_edit).hide()
        self.__getattribute__(del_button).hide()
