from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel
)
from PyQt5.QtGui import QColor


class TableModel(
    QAbstractTableModel
):

    def __init__(
        self,
        data,
        headers,
        highlight_errors=False
    ):

        super().__init__()

        self._data = data

        self._headers = headers
        self.highlight_errors = highlight_errors

    def rowCount(
        self,
        parent=None
    ):
        return len(self._data)

    def columnCount(
        self,
        parent=None
    ):
        return len(self._headers)

    def data(
            self,
            index,
            role
    ):

        value = self._data[
            index.row()
        ][
            index.column()
        ]

        if role == Qt.DisplayRole:
            return str(value)

        if role == Qt.TextAlignmentRole:
            return (
                    Qt.AlignCenter
                    | Qt.AlignVCenter
            )

        # if (
        #         self.highlight_errors
        #         and role == Qt.BackgroundRole
        # ):
        #
        #     if index.column() >= 5:
        #
        #         try:
        #
        #             if value != "" and int(value) > 0:
        #                 return QColor(
        #                     "#FFC7CE"
        #                 )
        #
        #         except:
        #             pass
        if role == Qt.BackgroundRole:

            # ====================================
            # Error Summary Table
            # ====================================

            if self.highlight_errors:

                if index.column() >= 5:

                    try:

                        if value != "" and int(value) > 0:
                            return QColor(
                                "#FFC7CE"
                            )

                    except:
                        pass

            # ====================================
            # Slot Yield Table
            # ====================================

            if (
                    len(self._headers) == 49
                    and self._headers[0] == "Item"
            ):

                # Prime Yield (%) row

                if (
                        index.row() == 4
                        and index.column() > 0
                        and value != ""
                ):

                    try:

                        yield_value = float(value)

                        if yield_value == 100:

                            return QColor(
                                "#C6EFCE"
                            )

                        elif yield_value >= 98:

                            return QColor(
                                "#FFEB9C"
                            )

                        else:

                            return QColor(
                                "#FFC7CE"
                            )

                    except:
                        pass

        return None


    def headerData(
        self,
        section,
        orientation,
        role
    ):

        if (
            role == Qt.DisplayRole
        ):

            if orientation == Qt.Horizontal:

                return self._headers[
                    section
                ]

        return None