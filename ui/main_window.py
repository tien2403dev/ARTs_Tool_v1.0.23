from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QTableView,
    QMessageBox,
    QProgressBar,
    QTabWidget,
    QComboBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
    QHeaderView,
    QFormLayout,
    QDateEdit,
    QLineEdit,
QTableWidgetItem,
QTableWidget

)
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QScrollArea

from workers.import_worker import (
    ImportWorker
)

from services.sqlite_service import (
    SQLiteService
)

from ui.table_model import (
    TableModel
)
from widgets.yield_chart import YieldChart
from widgets.yield_month_chart import YieldMonthChart
from widgets.handler_zone_chart import HandlerZoneChart
from widgets.slot_yield_chart import SlotYieldChart
from widgets.slot_daily_chart import SlotDailyChart
from widgets.yield_fail_daily_chart import YieldFailDailyChart
from widgets.model_daily_chart import ModelDailyChart

from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import QSize


class ComboBoxDelegate(QStyledItemDelegate):

    def sizeHint(self, option, index):

        return QSize(
            super().sizeHint(option, index).width(),
            28
        )

class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.db = SQLiteService()
        self.loading_filters = False

        self.init_ui()
        self.load_filter_values()
        self.load_scrap_filter()

    def create_label(self, text):

        label = QLabel(text)

        label.setStyleSheet("""
            font-size: 10pt;
        """)

        return label
    def init_ui(self):

        self.resize(
            1400,
            800
        )

        self.setWindowTitle(
            "Yield ARTs App"
        )

        self.btn_load = QPushButton(
            "Import Excel"
        )
        self.btn_export = QPushButton(
            "Export Excel"
        )
        self.btn_apply_filter = QPushButton(
            "Apply Filter"
        )

        # ================BO LOC
        self.cmb_eqp = QComboBox()
        self.cmb_handler = QComboBox()
        self.cmb_zone = QComboBox()
        self.cmb_slot = QComboBox()
        self.cmb_model = QComboBox()
        self.cmb_date = QComboBox()
        self.date_from = QDateEdit()
        self.date_to = QDateEdit()
        self.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #C0C0C0;
                border-radius: 4px;
                padding-left: 5px;
            }
        """)

        for widget in [
            self.date_from,
            self.date_to
        ]:
            widget.setCalendarPopup(True)
            widget.setDisplayFormat("yyyy-MM-dd")
            widget.setMinimumHeight(32)

        self.btn_apply_filter.setMinimumHeight(32)
        self.btn_apply_filter.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
                QPushButton:hover {
                background-color: #1E90FF;
            }
            
        """)
        self.btn_load.setMinimumHeight(32)
        self.btn_load.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #1E90FF;
            }
        """)
        self.btn_export.setMinimumHeight(32)
        self.btn_export.setStyleSheet("""
                    QPushButton {
                        background-color: #0078D7;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #1E90FF;
                    }
                """)

        self.scrap_filter = QListWidget()
        self.scrap_filter.setMaximumWidth(180)
        self.scrap_filter.setMinimumWidth(150)
        self.scrap_filter.setFixedHeight(100)

        for combo in [
            self.cmb_eqp,
            self.cmb_handler,
            self.cmb_zone,
            self.cmb_slot,
            self.cmb_model,
            self.cmb_date
        ]:
            combo.setMinimumHeight(28)
            combo.setMinimumWidth(200)
            font = combo.font()
            font.setPointSize(9)
            combo.setFont(font)

            combo.setItemDelegate(
                ComboBoxDelegate(combo)
            )
            combo.addItem("All")

        #TẠO LAYOUT CHO BỘ LỌC

        filter_layout = QGridLayout()
        filter_layout.setContentsMargins(
            0, 0, 0, 10
        )

        filter_layout.addWidget(
            self.create_label("Date From"),
            0,
            0
        )

        filter_layout.addWidget(
            self.date_from,
            0,
            1
        )

        filter_layout.addWidget(
            self.create_label("Date To"),
            0,
            2
        )

        filter_layout.addWidget(
            self.date_to,
            0,
            3
        )
        filter_layout.addWidget(
            self.create_label("EQP"),
            0,
            4
        )

        filter_layout.addWidget(
            self.cmb_eqp,
            0,
            5
        )

        filter_layout.addWidget(
            self.create_label("Handler"),
            0,
            6
        )

        filter_layout.addWidget(
            self.cmb_handler,
            0,
            7
        )

        filter_layout.addWidget(
            self.create_label("Zone"),
            1,
            0
        )

        filter_layout.addWidget(
            self.cmb_zone,
            1,
            1
        )

        filter_layout.addWidget(
            self.create_label("Slot"),
            1,
            2
        )

        filter_layout.addWidget(
            self.cmb_slot,
            1,
            3
        )

        filter_layout.addWidget(
            self.create_label("Model"),
            1,
            4
        )

        filter_layout.addWidget(
            self.cmb_model,
            1,
            5
        )

        filter_layout.addWidget(
            self.create_label("Date"),
            1,
            6
        )

        filter_layout.addWidget(
            self.cmb_date,
            1,
            7
        )
        ##ERROR CODE
        filter_layout.addWidget(
            self.create_label("Error Code"),
            0,
            8
        )

        filter_layout.addWidget(
            self.scrap_filter,
            0,
            9,
            3,
            1
        )
        filter_layout.addWidget(
            self.btn_load,
            3,
            0
        )
        filter_layout.addWidget(
            self.btn_export,
            3,
            1
        )

        filter_layout.addWidget(
            self.btn_apply_filter,
            3,
            9
        )

        filter_layout.setHorizontalSpacing(
            15
        )
        filter_layout.setVerticalSpacing(
            20
        )

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                min-width: 100px;
                min-height: 32px;
                padding: 0px 10px;
                background: white;
                border: none;
                }
        
            QTabBar::tab:selected {
                border-bottom: 3px solid #0078D7;
                font-weight: bold;
            }
        """)
        # =====================
        # TABS INPUT
        self.input_table = QTableView()


        ##=====SUMMARY
        self.summary_title = QLabel()
        self.summary_table = QTableView()
        self.ppm_title = QLabel()
        self.ppm_title.setStyleSheet(
            """
            font-weight: bold;
            font-size: 12px;
            """
        )
        self.ppm_table = QTableView()

        # ==========================
        # ANALYZE TAB
        # ==========================

        self.analyze_page = QWidget()
        self.analyze_layout = QVBoxLayout()

        # Yield ARTs table
        self.analyze_title = QLabel("Yield ARTs machine on month")
        self.analyze_title.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            """
        )
        self.analyze_table = QTableView()
        self.analyze_table.setMinimumHeight(450)

        self.analyze_layout.addWidget(
            self.analyze_title
        )

        self.chart = YieldChart()
        self.chart.setMinimumHeight(450)

        row_layout = QHBoxLayout()

        row_layout.addWidget(
            self.chart,
            5
        )
        row_layout.addWidget(
            self.analyze_table,
            2
        )

        self.analyze_row_widget = QWidget()
        self.analyze_row_widget.setLayout(
            row_layout
        )

        self.analyze_layout.addWidget(
            self.analyze_row_widget
        )
        # self.analyze_layout.addStretch()  ###tu dan het chieu rong

        ###BIEU DO HIEN THI MA LOI HANG NGAY
        self.daily_title = QLabel(
            "Yield ARTs machine on day"
        )
        self.daily_title.setStyleSheet(
            """
            font-size:14px;
            font-weight:bold;
            """
        )

        self.daily_table = QTableView()
        self.daily_chart = YieldChart()
        self.daily_chart.setMinimumHeight(450)

        daily_row_layout = QHBoxLayout()
        daily_row_layout.addWidget(
            self.daily_chart,
            5
        )

        daily_row_layout.addWidget(
            self.daily_table,
            2
        )

        self.daily_row_widget = QWidget()

        self.daily_row_widget.setLayout(
            daily_row_layout
        )

        self.analyze_layout.addWidget(
            self.daily_title
        )

        self.analyze_layout.addWidget(
            self.daily_row_widget
        )

        self.analyze_page.setLayout(
            self.analyze_layout
        )

        # ===================================
        # BIEU DO MA LOI THANG
        # ===================================
        self.ppm_monitor_title = QLabel(
            "Yield ARTs By EQP"
        )

        self.ppm_monitor_title.setStyleSheet(
            """
            font-size:14px;
            font-weight:bold;
            """
        )

        self.ppm_monitor_chart = YieldMonthChart()

        self.ppm_monitor_chart.setMinimumHeight(450)

        self.analyze_layout.addWidget(
            self.ppm_monitor_title
        )

        self.analyze_layout.addWidget(
            self.ppm_monitor_chart
        )

        ###BIEU DO CHO 4 HANDLER
        self.handler_monitor_groups = []  ###tạo cho 4 Handler
        for handler_no in range(1, 5):
            title = QLabel(
                f"Yield ARTs By Handler {handler_no}"
            )

            title.setStyleSheet(
                """
                font-size:12px;
                font-weight:bold;
                """
            )

            chart = YieldMonthChart()

            chart.setMinimumHeight(
                450
            )

            self.analyze_layout.addWidget(
                title
            )

            self.analyze_layout.addWidget(
                chart
            )

            self.handler_monitor_groups.append(
                {
                    "handler": handler_no,
                    "title": title,
                    "chart": chart
                }
            )
        #### SLOT ON MONTH TABLE
        self.slot_yield_title = QLabel(
            "Yield Slot On Month"
        )

        self.slot_yield_table = QTableView()

        self.analyze_layout.addWidget(
            self.slot_yield_title
        )
        self.slot_yield_title.setStyleSheet(
            """
            font-size:12px;
            font-weight:bold;
            """
        )

        self.analyze_layout.addWidget(
            self.slot_yield_table
        )
        ###SLOT ON MONTH BIEU DO

        self.slot_yield_chart = SlotYieldChart()
        self.slot_yield_chart_title = QLabel(
            "Yield Slot On Month"
        )
        self.slot_yield_chart_title.setStyleSheet("""
            font-size: 8pt;
            font-weight: bold;
            
        """)



        self.slot_chart_scroll = QScrollArea()

        self.slot_chart_scroll.setWidget(
            self.slot_yield_chart
        )

        self.slot_chart_scroll.setWidgetResizable(
            False
        )

        self.slot_chart_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.slot_chart_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )
        self.slot_chart_scroll.setFixedHeight(
            450
        )
        self.analyze_layout.addWidget(
            self.slot_yield_chart_title
        )
        self.analyze_layout.addWidget(
            self.slot_chart_scroll
        )

        ###table cho slot on daily
        self.slot_daily_title = QLabel(
            "Yield Slot On Day"
        )
        self.slot_daily_title.setStyleSheet(
            """
            font-size:12px;
            font-weight:bold;
            """
        )

        self.slot_daily_table = QTableView()

        self.analyze_layout.addWidget(
            self.slot_daily_title
        )

        self.analyze_layout.addWidget(
            self.slot_daily_table
        )
        self.slot_daily_table.setFixedHeight(
            160
        )

        ###BIEU DO SLOT ON DAY
        self.slot_daily_chart = SlotYieldChart()
        self.slot_daily_chart_title = QLabel()

        self.slot_daily_chart_title.setStyleSheet("""
            font-size: 12pt;
            font-weight: bold;
        """)

        self.analyze_layout.addWidget(
            self.slot_daily_chart_title
        )

        self.slot_daily_chart_scroll = QScrollArea()

        self.slot_daily_chart_scroll.setWidget(
            self.slot_daily_chart
        )

        self.slot_daily_chart_scroll.setWidgetResizable(
            False
        )

        self.slot_daily_chart_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.slot_daily_chart_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.slot_daily_chart_scroll.setFixedHeight(
            450
        )

        self.analyze_layout.addWidget(
            self.slot_daily_chart_scroll
        )

        ####TABLE 1 SLOT TUNG NGAY TRONG THANG
        self.slot_daily_analyze = QLabel()
        self.slot_daily_total_label = QLabel()

        self.slot_daily_total_label.setStyleSheet("""
            QLabel{
                font-weight:bold;
                font-size:12pt;
            }
        """)
        self.slot_daily_analyze.setStyleSheet("""
            QLabel{
                font-weight:bold;
                font-size:12pt;
            }
        """)
        self.analyze_layout.addWidget(
            self.slot_daily_analyze
        )
        self.analyze_layout.addWidget(
            self.slot_daily_total_label
        )
        self.slot_daily_analysis_table = QTableView()
        self.slot_daily_analysis_table.setFixedHeight(720)

        self.analyze_layout.addWidget(
            self.slot_daily_analysis_table
        )
        ###BIEU DO 1 SLOT TUNG NGAY TRONG THANG
        self.yield_slot_chart = SlotDailyChart()
        self.yield_slot_chart_title = QLabel()
        self.yield_slot_chart_title.setStyleSheet("""
                    QLabel{
                        font-weight:bold;
                        font-size:12pt;
                    }
                """)

        self.yield_slot_chart.setFixedHeight(
            450
        )
        self.analyze_layout.addWidget(
            self.yield_slot_chart_title
        )

        self.analyze_layout.addWidget(
            self.yield_slot_chart
        )
        ###HIEN THI MA LOI TAT CA THIET BI TUNG NGAY TRONG THANG
        self.yield_fail_daily_title = QLabel(
            "Yield Fail Qty Daily"
        )

        self.yield_fail_daily_title.setStyleSheet(
            """
            font-size:12px;
            font-weight:bold;
            """
        )

        # self.yield_fail_daily_total_label = QLabel()

        self.yield_fail_daily_table = QTableView()
        self.yield_fail_daily_table.setFixedHeight(790)

        self.analyze_layout.addWidget(
            self.yield_fail_daily_title
        )

        # self.analyze_layout.addWidget(
        #     self.yield_fail_daily_total_label
        # )

        self.analyze_layout.addWidget(
            self.yield_fail_daily_table
        )
        ####BIEU DO MA LOI TAT CA THIET BI TUNG NGAY TRONG THANG
        self.yield_fail_daily_chart_title = QLabel(
            "Yield Fail Qty Daily Chart"
        )

        self.yield_fail_daily_chart_title.setStyleSheet(
            """
            font-size:12px;
            font-weight:bold;
            """
        )

        self.yield_fail_daily_chart = YieldFailDailyChart()
        self.yield_fail_daily_chart.setFixedHeight(
            450
        )
        self.analyze_layout.addWidget(
            self.yield_fail_daily_chart_title
        )

        self.analyze_layout.addWidget(
            self.yield_fail_daily_chart
        )

        ####THONG KE TUNG MA SAN PHAM TREN TUNG THIET BI
        self.model_daily_title = QLabel(
            "Model Daily Summary"
        )

        self.model_daily_title.setStyleSheet(
            """
            font-size:12px;
            font-weight:bold;
            """
        )

        self.model_daily_table = QTableView()
        self.model_daily_table.setFixedHeight(790)
        self.analyze_layout.addWidget(
            self.model_daily_title
        )

        self.analyze_layout.addWidget(
            self.model_daily_table
        )
        ####BIEU DO CHO TUNG MODEL
        self.model_daily_chart = ModelDailyChart()
        self.model_daily_chart_title = QLabel()
        self.model_daily_chart_title.setStyleSheet(
            """
            font-size:12px;
            font-weight:bold;
            """
        )
        self.analyze_layout.addWidget(
            self.model_daily_chart_title
        )
        self.analyze_layout.addWidget(
            self.model_daily_chart
        )

        self.model_daily_chart.setFixedHeight(
            450
        )



        # Scroll bar cho tab analyze
        self.analyze_scroll = QScrollArea()

        self.analyze_scroll.setWidgetResizable(
            True
        )

        self.analyze_scroll.setWidget(
            self.analyze_page
        )

        self.chart.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        self.tabs.addTab(
            self.analyze_scroll,
            "Analyze"
        )

        ###=========TAB INPUT
        # self.tabs.addTab(
        #     self.input_table,
        #     "Input"
        # )

        ####==========TAB HANDLER
        ###TẠO CHO CẢ TABLE VÀ CHART
        self.handler_page = QWidget()

        handler_layout = QVBoxLayout()

        self.handler_groups = []

        for handler_no in range(1, 5):

            # ==========================
            # Titles
            # ==========================

            monthly_title = QLabel()
            daily_title = QLabel()

            title_style = """
                font-weight: bold;
                font-size: 12px;
            """

            monthly_title.setStyleSheet(title_style)
            daily_title.setStyleSheet(title_style)

            # ==========================
            # Monthly Widgets
            # ==========================

            monthly_table = QTableView()
            monthly_chart = HandlerZoneChart()

            # ==========================
            # Daily Widgets
            # ==========================

            daily_table = QTableView()
            daily_chart = HandlerZoneChart()

            # ==========================
            # Fixed Height
            # ==========================

            HEIGHT = 350

            monthly_table.setFixedHeight(HEIGHT)
            monthly_chart.setFixedHeight(HEIGHT)

            daily_table.setFixedHeight(HEIGHT)
            daily_chart.setFixedHeight(HEIGHT)

            # ==========================
            # Table Settings
            # ==========================

            for table in [monthly_table, daily_table]:
                table.setVerticalScrollBarPolicy(
                    Qt.ScrollBarAlwaysOff
                )

                table.setHorizontalScrollBarPolicy(
                    Qt.ScrollBarAlwaysOff
                )

            # ==========================
            # Monthly Block
            # ==========================

            monthly_block = QVBoxLayout()

            monthly_block.addWidget(
                monthly_title
            )

            monthly_row = QHBoxLayout()

            monthly_row.addWidget(
                monthly_table,
                2
            )

            monthly_row.addWidget(
                monthly_chart,
                6
            )

            monthly_block.addLayout(
                monthly_row
            )

            # ==========================
            # Daily Block
            # ==========================

            daily_block = QVBoxLayout()

            daily_block.addWidget(
                daily_title
            )

            daily_row = QHBoxLayout()

            daily_row.addWidget(
                daily_table,
                2
            )

            daily_row.addWidget(
                daily_chart,
                6
            )

            daily_block.addLayout(
                daily_row
            )

            # ==========================
            # Main Row
            # ==========================

            main_row = QHBoxLayout()

            main_row.addLayout(
                monthly_block,
                1
            )

            main_row.addLayout(
                daily_block,
                1
            )

            handler_layout.addLayout(
                main_row
            )

            handler_layout.addSpacing(
                20
            )

            # ==========================
            # Save Widgets
            # ==========================

            self.handler_groups.append(
                {
                    "handler": handler_no,

                    "monthly_title": monthly_title,
                    "monthly_table": monthly_table,
                    "monthly_chart": monthly_chart,

                    "daily_title": daily_title,
                    "daily_table": daily_table,
                    "daily_chart": daily_chart
                }
            )

        handler_layout.addStretch()

        self.handler_page.setLayout(
            handler_layout
        )

        # ==========================
        # Scroll Area
        # ==========================

        self.handler_scroll = QScrollArea()

        self.handler_scroll.setWidgetResizable(
            True
        )

        self.handler_scroll.setWidget(
            self.handler_page
        )

        self.tabs.addTab(
            self.handler_scroll,
            "Handler"
        )

        ####========TAB SUMMARY
        self.summary_page = QWidget()

        summary_layout = QVBoxLayout()

        self.summary_title.setStyleSheet(
            """
            font-weight: bold;
            font-size: 12px;
            """
        )

        summary_layout.addWidget(
            self.summary_title
        )

        summary_layout.addWidget(
            self.summary_table
        )

        summary_layout.addWidget(
            self.ppm_title
        )

        summary_layout.addWidget(
            self.ppm_table
        )

        self.handler_summary_groups = []
        for handler_no in range(1, 5):
            handler_title = QLabel(
                f"Handler {handler_no}"
            )

            handler_title.setStyleSheet(
                """
                font-size: 12px;
                font-weight: bold;
                """
            )

            error_title = QLabel()
            error_title.setStyleSheet(
                """
                font-weight: bold;
                font-size: 12px;
                """
            )

            ppm_title = QLabel()
            ppm_title.setStyleSheet(
                """
                font-weight: bold;
                font-size: 12px;
                """
            )

            error_table = QTableView()

            ppm_table = QTableView()

            summary_layout.addWidget(
                handler_title
            )

            summary_layout.addWidget(
                error_title
            )

            summary_layout.addWidget(
                error_table
            )

            summary_layout.addWidget(
                ppm_title
            )

            summary_layout.addWidget(
                ppm_table
            )

            summary_layout.addSpacing(
                20
            )

            self.handler_summary_groups.append(
                {
                    "error_title": error_title,
                    "error_table": error_table,
                    "ppm_title": ppm_title,
                    "ppm_table": ppm_table
                }
            )

        self.summary_page.setLayout(
            summary_layout
        )
        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setWidget(
            self.summary_page
        )

        self.tabs.addTab(
            scroll,
            "Summary"
        )

        layout = QVBoxLayout()

        # layout.addWidget(
        #     self.btn_load
        # )
        #
        # layout.addWidget(
        #     self.progress
        # )
        ####==========TAB DATABASE MANAGEMENT
        self.database_page = QWidget()

        self.create_database_page()

        self.tabs.addTab(
            self.database_page,
            "Database Management"
        )

        layout.addLayout(
            filter_layout
        )

        layout.addWidget(
            self.tabs
        )

        self.setLayout(layout)

        #######=======LOAD FILE EXCEL
        self.btn_load.clicked.connect(
            self.load_files
        )

        ###=======SU DUNG NUT DE APPLY BO LOC
        self.btn_apply_filter.clicked.connect(
            self.apply_all_filters
        )

        self.date_from.dateChanged.connect(
            self.load_filter_dates
        )

        self.date_to.dateChanged.connect(
            self.load_filter_dates
        )

    def load_files(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Excel Files",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not files:
            return

        self.worker = ImportWorker(
            files
        )

        # self.worker.progress.connect(
        #     self.progress.setValue
        # )

        self.worker.finished.connect(
            self.load_table
        )

        self.worker.error.connect(
            self.show_error
        )

        self.worker.start()



    def load_table(self):

        ##khong hien thi len input nua
        data = self.db.get_all_data()

        headers = self.db.get_headers()

        model = TableModel(
            data,
            headers
        )

        self.input_table.setModel(model)

        self.loading_filters = True
        self.load_filter_values()
        self.load_filter_dates()
        self.load_scrap_filter()
        self.loading_filters = False
        ##tab analyze
        self.load_analyze_table() #chua cho hien thi

        QMessageBox.information(
            self,
            "Done",
            "Import Success"
        )




    ####LOAD DỮ LIỆU CHO BỘ LỌC
    def load_filter_values(self):

        self.cmb_eqp.blockSignals(True)
        self.cmb_eqp.clear()
        self.cmb_handler.clear()
        self.cmb_zone.clear()
        self.cmb_slot.clear()
        self.cmb_model.clear()
        self.cmb_date.clear()

        self.cmb_eqp.addItem("Chọn EQP")
        self.cmb_handler.addItem("Chọn Handler")
        self.cmb_zone.addItem("Chọn Zone")
        self.cmb_slot.addItem("Chọn Slot")
        self.cmb_model.addItem("Chọn Model")
        self.cmb_date.addItem("Chọn ngày")

        self.cmb_eqp.addItems(
            self.db.get_distinct_values(
                "EQP"
            )
        )

        self.cmb_handler.addItems(
            self.db.get_distinct_values(
                "Handler"
            )
        )

        self.cmb_zone.addItems(
            self.db.get_distinct_values(
                "ZONE"
            )
        )

        self.cmb_slot.addItems(
            self.db.get_distinct_values(
                "SLOT"
            )
        )

        self.cmb_model.addItems(
            self.db.get_distinct_values(
                "Model"
            )
        )

        # self.cmb_date.addItems(
        #     self.db.get_distinct_values(
        #         "File_Date"
        #     )
        # )
        self.cmb_eqp.blockSignals(False)


    ##LOAD dữ liệu cho mã lỗi
    def load_scrap_filter(self):
        self.scrap_filter.blockSignals(True)
        self.scrap_filter.clear()

        codes = self.db.get_scrap_codes()

        for code in codes:
            item = QListWidgetItem(code)

            item.setCheckState(
                0
            )

            self.scrap_filter.addItem(
                item
            )
        self.scrap_filter.blockSignals(False)

    def show_error(
        self,
        msg
    ):

        QMessageBox.critical(
            self,
            "Error",
            msg
        )
    ###HAM APPLY FILTER
    def apply_all_filters(self):

        if not self.validate_date_range():
            return


        self.load_summary_table()
        print("1")
        self.load_handler_summary_tables()
        print("2")
        self.load_daily_analyze_table()
        print("3")
        self.load_ppm_monitor_chart()
        print("4")
        self.load_handler_monitor_chart()
        print("5")
        self.load_analyze_table()
        print("6")
        self.load_handler_data()
        print("7")
        self.load_slot_yield_table()
        print("8")
        self.load_slot_yield_chart()
        print("9")
        self.load_slot_daily_table()
        print("10")
        self.load_slot_daily_chart()
        print("11")
        self.load_slot_daily_analysis_table()
        print("12")
        self.load_yield_slot_chart()
        print("13")
        self.load_yield_fail_daily_table()
        print("14")
        self.load_yield_fail_daily_chart()
        print("15")
        self.load_model_daily_table()
        print("16")
        self.load_model_daily_chart()
        print("DONE")
        self.date_to_selected = True


    ####HAM LAY KHOANG NGAY CHO BO LOC NGAY
    def get_date_range(self):

        date_from = (
            self.date_from.date()
            .toString("yyyyMMdd")
        )

        date_to = (
            self.date_to.date()
            .toString("yyyyMMdd")
        )

        return date_from, date_to

    def validate_date_range(self):

        date_from = self.date_from.date()
        date_to = self.date_to.date()

        if date_from.year() == 2000:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select Date From"
            )
            return False

        if date_to.year() == 2000:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select Date To"
            )
            return False

        if date_from > date_to:
            QMessageBox.warning(
                self,
                "Warning",
                "Date From must <= Date To"
            )
            return False

        return True

    def load_filter_dates(self):

        date_from, date_to = (
            self.get_date_range()
        )

        dates = self.db.get_dates_in_range(
            date_from,
            date_to
        )

        self.cmb_date.blockSignals(True)

        self.cmb_date.clear()

        self.cmb_date.addItem(
            "Chọn ngày"
        )

        self.cmb_date.addItems(
            dates
        )

        self.cmb_date.blockSignals(False)
    ###HET PHAN XU LY CHO BO LOC

    #######TAB SUMMARY##########
    ####LOAD DU LIEU TAB SUMMARY (TAT CA)
    def load_summary_table(self):

        eqp = self.cmb_eqp.currentText()
        date_from, date_to = self.get_date_range()
        if eqp in ["", "Chọn EQP"]:
            self.summary_title.setText(
                "Daily Yield & Error Summary by EQP"
            )

            self.ppm_title.setText(
                "Daily Error PPM Summary by EQP"
            )

            empty_headers = [
                "Date",
                "In",
                "Out",
                "Fail",
                "Cum Yield"
            ]

            self.summary_table.setModel(
                TableModel(
                    [],
                    empty_headers
                )
            )

            self.ppm_table.setModel(
                TableModel(
                    [],
                    empty_headers
                )
            )

            self.summary_table.setFixedHeight(400)

            self.ppm_table.setFixedHeight(400)

            return

        self.summary_title.setText(
            f"Daily Yield & Error Summary by EQP | EQP = {eqp}"
        )

        if eqp in [
            "",
            "Chọn EQP"
        ]:
            return

        headers = self.db.get_summary_headers()

        data = self.db.get_summary_data(
            eqp,
            date_from,
            date_to
        )

        model = TableModel(
            data,
            headers,
            highlight_errors=True
        )

        self.summary_table.setModel(
            model
        )
        self.summary_table.resizeRowsToContents()

        height = (
                self.summary_table.horizontalHeader().height()
                +
                self.summary_table.rowHeight(0)
                * len(data)
                + 5
        )

        self.summary_table.setFixedHeight(
            height
        )

        self.summary_table.resizeColumnsToContents()
        self.summary_table.verticalHeader().setDefaultSectionSize(
            18
        )
        self.summary_table.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.summary_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        ####PPM
        self.ppm_title.setText(
            f"Daily Error PPM Summary by EQP | EQP = {eqp}"
        )
        ppm_headers = self.db.get_ppm_headers()

        ppm_data = self.db.get_ppm_summary_data(
            data
        )

        self.ppm_table.setModel(
            TableModel(
                ppm_data,
                ppm_headers,
                highlight_errors=True
            )
        )

        self.ppm_table.resizeColumnsToContents()
        self.ppm_table.verticalHeader().setDefaultSectionSize(
            18
        )
        self.ppm_table.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.ppm_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )
        self.ppm_table.resizeRowsToContents()

        height = (
                self.ppm_table.horizontalHeader().height()
                +
                self.ppm_table.rowHeight(0)
                * len(ppm_data)
                + 5
        )

        self.ppm_table.setFixedHeight(
            height
        )
    ####LOAD DU LIEU TAB SUMMARY (4 HANDLER)
    def load_handler_summary_tables(self):

        eqp = self.cmb_eqp.currentText()
        date_from, date_to = self.get_date_range()
        if eqp in ["", "Chọn EQP"]:

            headers = [
                "Date",
                "In",
                "Out",
                "Fail",
                "Cum Yield"
            ]

            for handler_no in range(1, 5):
                group = self.handler_summary_groups[
                    handler_no - 1
                    ]

                group["error_title"].setText("")
                group["ppm_title"].setText("")

                group["error_table"].setModel(
                    TableModel(
                        [],
                        headers
                    )
                )

                group["ppm_table"].setModel(
                    TableModel(
                        [],
                        headers
                    )
                )

                group["error_table"].setFixedHeight(400)
                group["ppm_table"].setFixedHeight(400)

            return

        headers = self.db.get_summary_headers()

        for handler_no in range(1, 5):
            group = self.handler_summary_groups[
                handler_no - 1
                ]

            group["error_title"].setText(
                f"Handler {handler_no} Daily Error Summary | EQP = {eqp}"
            )

            error_data = self.db.get_handler_summary_data(
                eqp,
                handler_no,
                date_from,
                date_to
            )

            ppm_data = self.db.get_handler_ppm_summary_data(
                error_data
            )

            group["error_table"].setModel(
                TableModel(
                    error_data,
                    headers,
                    highlight_errors=True
                )
            )

            group["error_table"].resizeColumnsToContents()
            group["error_table"].resizeRowsToContents()

            error_height = (
                    group["error_table"].horizontalHeader().height()
                    +
                    group["error_table"].rowHeight(0)
                    * len(error_data)
                    + 5
            )

            group["error_table"].setFixedHeight(
                error_height
            )

            group["ppm_title"].setText(
                f"Handler {handler_no} Daily PPM Summary | EQP = {eqp}"
            )

            group["ppm_table"].setModel(
                TableModel(
                    ppm_data,
                    headers,
                    highlight_errors=True

                )
            )

            group["ppm_table"].resizeColumnsToContents()
            group["ppm_table"].resizeRowsToContents()

            ppm_height = (
                    group["ppm_table"].horizontalHeader().height()
                    +
                    group["ppm_table"].rowHeight(0)
                    * len(ppm_data)
                    + 5
            )

            group["ppm_table"].setFixedHeight(
                ppm_height
            )
    ####=======HET TAB SUMMARY

    ####========TAB HANDLER
    ###HIEN THI BIEU DO VA DU LIEU CHO MONTHLY VA DAILY (GOP 2 HAM, 1 HAM LAY DU LIEU CHO TABLE, 1 HAM VE BIEU DO THANH 1 VI CA 2 CUNG LAY CHUNG 1 SQL)
    def load_handler_data(self):

        if self.loading_filters:
            return

        eqp = self.cmb_eqp.currentText()

        date = self.cmb_date.currentText()

        date_from, date_to = self.get_date_range()

        headers = [
            "Zone",
            "In",
            "Pass",
            "Fail",
            "Yield"
        ]

        # ==========================
        # CLEAR
        # ==========================

        if eqp in ["", "Chọn EQP"]:

            for group in self.handler_groups:
                group["monthly_table"].setModel(
                    TableModel([], headers)
                )

                group["daily_table"].setModel(
                    TableModel([], headers)
                )

                group["monthly_title"].setText("")
                group["daily_title"].setText("")

                group["monthly_chart"].clear_chart()
                group["daily_chart"].clear_chart()

            return

        # ==========================
        # LOAD DATA
        # ==========================

        for group in self.handler_groups:

            handler_no = group["handler"]

            # ======================================
            # MONTHLY DATA
            # ======================================

            monthly_data = self.db.get_handler_monthly_summary(
                eqp,
                handler_no,
                date_from,
                date_to
            )

            group["monthly_title"].setText(
                f"Handler {handler_no} Zone Yield Monitoring on month | EQP: {eqp}"
            )

            # TABLE

            group["monthly_table"].setModel(
                TableModel(
                    monthly_data,
                    headers
                )
            )

            group["monthly_table"].resizeColumnsToContents()
            group["monthly_table"].resizeRowsToContents()

            monthly_table = group["monthly_table"]

            monthly_height = (
                    monthly_table.horizontalHeader().height()
                    + monthly_table.horizontalHeader().height()
            )

            for row in range(
                    monthly_table.model().rowCount()
            ):
                monthly_height += monthly_table.rowHeight(
                    row
                )

            monthly_table.setFixedHeight(
                monthly_height
            )

            monthly_table.verticalHeader().setSectionResizeMode(
                QHeaderView.Stretch
            )

            # CHART

            group["monthly_chart"].plot_data(
                monthly_data
            )

            # ======================================
            # DAILY DATA
            # ======================================

            if date in ["", "Chọn ngày"]:

                daily_data = []

                group["daily_title"].setText(
                    f"Handler {handler_no} Zone Yield Monitoring on day"
                )

                group["daily_chart"].clear_chart()

            else:

                daily_data = self.db.get_handler_daily_summary(
                    eqp,
                    handler_no,
                    date
                )

                group["daily_title"].setText(
                    f"Handler {handler_no} Zone Yield Monitoring on day | EQP: {eqp} & Date: {date}"
                )

                group["daily_chart"].plot_data(
                    daily_data
                )

            # TABLE

            group["daily_table"].setModel(
                TableModel(
                    daily_data,
                    headers
                )
            )

            group["daily_table"].resizeColumnsToContents()
            group["daily_table"].resizeRowsToContents()

            daily_table = group["daily_table"]

            daily_table.setFixedHeight(
                monthly_height
            )

            daily_table.verticalHeader().setSectionResizeMode(
                QHeaderView.Stretch
            )
    ####HET TAB HANDLER============


    #####=======TAB ANALYZE
    ###load hieu suat cac may ca thang
    def load_analyze_table(self):

        self.analyze_title.setText(
            "Yield ARTs machine on month"
        )
        date_from, date_to = (
            self.get_date_range()
        )

        headers = self.db.get_monthly_eqp_headers()

        data = self.db.get_monthly_eqp_summary(
            date_from,
            date_to
        )

        self.analyze_table.setModel(
            TableModel(
                data,
                headers
            )
        )
        self.analyze_table.resizeColumnsToContents()
        self.chart.plot_data(data)

        self.chart.setMinimumHeight(450)
        self.chart.setMaximumHeight(450)

        self.analyze_row_widget.setFixedHeight(450)

    ###LOAD HIEU SUAT HANG NGAY
    def load_daily_analyze_table(self):


        date = self.cmb_date.currentText()

        if date in ["", "Chọn ngày"]:
            self.daily_title.setText(
                "Yield ARTs machine on day"
            )

            headers = self.db.get_monthly_eqp_headers()

            self.daily_table.setModel(
                TableModel([], headers)
            )

            self.daily_chart.clear_chart()

            return

        self.daily_title.setText(
            f"Yield ARTs machine on day | Date: {date}"  ##EQP: {eqp} &
        )

        data = self.db.get_daily_eqp_summary(
            date
        )

        headers = self.db.get_monthly_eqp_headers()

        self.daily_table.setModel(
            TableModel(
                data,
                headers
            )
        )

        self.daily_table.resizeColumnsToContents()

        self.daily_chart.plot_data(
            data
        )
        # self.daily_table.resizeRowsToContents()
        self.daily_table.setFixedHeight(450)

        self.daily_chart.setMinimumHeight(450)
        self.daily_chart.setMaximumHeight(450)

    ###Load BIEU DO MA LOI MAY DUOC CHON
    def get_selected_scrap_codes(self):

        result = []

        for i in range(
                self.scrap_filter.count()
        ):

            item = self.scrap_filter.item(i)

            if item.checkState():
                result.append(
                    item.text()
                )

        return result

    def load_ppm_monitor_chart(self):

        eqp = self.cmb_eqp.currentText()
        if eqp in ["", "All", "Chọn EQP"]:
            return

        # print("EQP =", eqp)
        self.ppm_monitor_title.setText(
            f"Yield ARTs By EQP | EQP: {eqp}"  ##EQP: {eqp} &
        )
        date_from, date_to = (
            self.get_date_range()
        )

        summary_data = (
            self.db.get_summary_data(
                eqp,
                date_from,
                date_to
            )
        )

        ppm_data = self.db.get_ppm_summary_data(
            summary_data
        )

        self.current_ppm_data = ppm_data

        self.ppm_monitor_chart.plot_data(
            ppm_data,
            self.get_selected_scrap_codes(),
            self.db.get_scrap_codes()
        )

    def load_handler_monitor_chart(self):

        eqp = self.cmb_eqp.currentText()

        selected_codes = (
            self.get_selected_scrap_codes()
        )

        all_codes = (
            self.db.get_scrap_codes()
        )
        date_from, date_to = (
            self.get_date_range()
        )

        for group in self.handler_monitor_groups:

            handler_no = group["handler"]

            group["title"].setText(
                f"Yield ARTs By Handler {handler_no} | EQP: {eqp}"
            )

            chart = group["chart"]

            summary_data = (
                self.db.get_handler_summary_data(
                    eqp,
                    handler_no,
                    date_from,
                    date_to
                )
            )

            ppm_data = (
                self.db.get_ppm_summary_data(
                    summary_data
                )
            )

            if ppm_data:
                chart.plot_data(
                    ppm_data,
                    selected_codes,
                    all_codes
                )
    ##HIEN THI TABLE SLOT THEO THANG
    def load_slot_yield_table(self):

        try:

            eqp = self.cmb_eqp.currentText()

            handler = self.cmb_handler.currentText()

            zone = self.cmb_zone.currentText()

            self.slot_yield_title.setText(
                f"Yield Slot On Month | EQP: {eqp} & Handler: {handler} & Zone: {zone}"
            )

            date_from, date_to = self.get_date_range()

            headers = self.db.get_slot_headers()

            data = self.db.get_slot_table_data(
                eqp=eqp,
                handler=handler,
                zone=zone,
                date_from=date_from,
                date_to=date_to
            )

            self.slot_yield_table.setModel(
                TableModel(
                    data,
                    headers
                )
            )

            self.slot_yield_table.resizeColumnsToContents()

            self.slot_yield_table.resizeRowsToContents()

            self.slot_yield_table.setFixedHeight(
                160
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "LOAD SLOT ERROR:",
                repr(e)
            )

    ##HIEN THI TABLE SLOT THEO NGAY
    def load_slot_daily_table(self):

        try:

            eqp = self.cmb_eqp.currentText()

            handler = self.cmb_handler.currentText()

            zone = self.cmb_zone.currentText()

            file_date = self.cmb_date.currentText()
            headers = self.db.get_slot_headers()
            if (
                    file_date in ["", "Chọn ngày"]
                    or eqp in ["", "Chọn EQP"]
                    or handler in ["", "Chọn Handler"]
                    or zone in ["", "Chọn Zone"]
            ):
                # self.slot_daily_title.setText(
                #     "Yield Slot On Day"
                # )

                self.slot_daily_table.setModel(
                    TableModel([], headers)
                )

                return

            self.slot_daily_title.setText(
                f"Yield Slot On Day | EQP: {eqp} & Handler: {handler} & Zone: {zone} & Date: {file_date}"
            )

            headers = self.db.get_slot_headers()

            data = self.db.get_slot_table_data(
                eqp=eqp,
                handler=handler,
                zone=zone,
                file_date=file_date
            )

            self.slot_daily_table.setModel(
                TableModel(
                    data,
                    headers
                )
            )

            self.slot_daily_table.resizeColumnsToContents()

            self.slot_daily_table.resizeRowsToContents()

            self.slot_daily_table.setFixedHeight(
                160
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "LOAD SLOT DAILY ERROR:",
                repr(e)
            )

    ###BIEU DO SLOT THEO THANG
    def load_slot_yield_chart(self):

        try:

            eqp = self.cmb_eqp.currentText()
            handler = self.cmb_handler.currentText()
            zone = self.cmb_zone.currentText()

            date_from, date_to = self.get_date_range()
            self.slot_yield_chart_title.setText(
                f"Yield Slot On Month | EQP: {eqp} & Handler: {handler} & Zone: {zone}"
            )
            slots, fails, yields = (
                self.db.get_slot_chart_data(
                    eqp=eqp,
                    handler=handler,
                    zone=zone,
                    date_from=date_from,
                    date_to=date_to
                )
            )

            self.slot_yield_chart.update_chart(
                slots,
                fails,
                yields,
                eqp,
                handler,
                zone
            )

        except Exception as e:

            import traceback
            traceback.print_exc()

            print(
                "LOAD SLOT CHART ERROR:",
                repr(e)
            )
    ####BIEU DO SLOT THEO  NGAY
    def load_slot_daily_chart(self):
        try:

            eqp = self.cmb_eqp.currentText()

            handler = self.cmb_handler.currentText()

            zone = self.cmb_zone.currentText()

            file_date = self.cmb_date.currentText()

            if (
                    not eqp
                    or not handler
                    or not zone
                    or not file_date
            ):
                return
            self.slot_daily_chart_title.setText(
                f"Yield Slot On Day | EQP: {eqp} & Handler: {handler} & Zone: {zone} & Date: {file_date}"
            )
            slots, fails, yields = (
                self.db.get_slot_chart_data(
                    eqp=eqp,
                    handler=handler,
                    zone=zone,
                    file_date=file_date
                )
            )

            self.slot_daily_chart.update_chart(
                slots,
                fails,
                yields,
                eqp,
                handler,
                zone
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "LOAD SLOT DAILY CHART ERROR:",
                repr(e)
            )
        ####TABLE 1 SLOT TUNG NGAY TRONG THANG
    def load_slot_daily_analysis_table(self):

        try:

            eqp = self.cmb_eqp.currentText()

            handler = self.cmb_handler.currentText()

            zone = self.cmb_zone.currentText()

            slot = self.cmb_slot.currentText()

            date_from, date_to = (
                self.get_date_range()
            )

            if (
                    not eqp
                    or not handler
                    or not zone
                    or not slot
            ):
                return

            headers = (
                self.db.get_slot_daily_headers()
            )

            data, total_fail, total_yield = (
                self.db.get_slot_daily_summary(
                    eqp,
                    handler,
                    zone,
                    slot,
                    date_from,
                    date_to
                )
            )
            self.slot_daily_analyze.setText(
                f"Yield Slot On Day | EQP: {eqp} & Handler: {handler} & Zone: {zone} & Slot: {slot}"
            )

            self.slot_daily_total_label.setText(
                f"Total Fail : {total_fail}  |  Yield : {total_yield:.2f}%"
            )

            self.slot_daily_analysis_table.setModel(
                TableModel(
                    data,
                    headers,
                    highlight_errors=True
                )
            )

            self.slot_daily_analysis_table.resizeColumnsToContents()

            self.slot_daily_analysis_table.resizeRowsToContents()

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "LOAD SLOT DAILY ANALYSIS ERROR:",
                repr(e)
            )

    def load_yield_slot_chart(self):

        eqp = self.cmb_eqp.currentText()

        handler = self.cmb_handler.currentText()

        zone = self.cmb_zone.currentText()

        slot = self.cmb_slot.currentText()
        self.yield_slot_chart_title.setText(
            f"Yield Slot On Day | EQP: {eqp} & Handler: {handler} & Zone: {zone} & Slot: {slot}"
        )

        date_from, date_to = self.get_date_range()

        selected_scraps = (
            self.get_selected_scrap_codes()
        )
        dates, yields, scrap_series = (
            self.db.get_slot_daily_chart_data(
                eqp,
                handler,
                zone,
                slot,
                date_from,
                date_to,
                selected_scraps
            )
        )
        self.yield_slot_chart.update_chart(
            dates,
            yields,
            scrap_series,
            eqp,
            handler,
            zone,
            slot
        )
    ####TONG HOP MA LOI TAT CA CAC MAY TUNG NGAY TRONG THANG
    def load_yield_fail_daily_table(self):

        try:

            date_from, date_to = (
                self.get_date_range()
            )

            headers = (
                self.db.get_yield_fail_daily_headers()
            )

            data, total_fail, total_yield  = (
                self.db.get_yield_fail_daily_data(
                    date_from,
                    date_to
                )
            )

            self.yield_fail_daily_title.setText(
                f"Yield Fail Qty Daily | {date_from} - {date_to}"
            )

            # self.yield_fail_daily_total_label.setText(
            #     f"Total Fail : {total_fail} | Yield : {total_yield:.2f}%"
            # )

            self.yield_fail_daily_table.setModel(
                TableModel(
                    data,
                    headers,
                    highlight_errors=True
                )
            )

            self.yield_fail_daily_table.resizeColumnsToContents()

            self.yield_fail_daily_table.resizeRowsToContents()

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "LOAD YIELD FAIL DAILY ERROR:",
                repr(e)
            )
    ###HAM LOAD BIEU DO MA LOI TAT CA CAC MAY TRONG THANG
    def load_yield_fail_daily_chart(self):

        try:

            date_from, date_to = (
                self.get_date_range()
            )

            selected_scraps = (
                self.get_selected_scrap_codes()
            )

            (
                dates,
                yields,
                scrap_series
            ) = self.db.get_yield_fail_daily_chart_data(
                date_from=date_from,
                date_to=date_to,
                selected_scraps=selected_scraps
            )

            self.yield_fail_daily_chart_title.setText(
                f"Yield Fail Qty Daily Chart | {date_from} ~ {date_to}"
            )

            self.yield_fail_daily_chart.update_chart(
                dates,
                yields,
                scrap_series
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "LOAD YIELD FAIL DAILY CHART ERROR:",
                repr(e)
            )
    ####THONG KE TUNG MA SAN PHAM TREN TUNG EQP
    def load_model_daily_table(self):

        try:

            model = self.cmb_model.currentText()

            eqp = self.cmb_eqp.currentText()

            handler = self.cmb_handler.currentText()

            zone = self.cmb_zone.currentText()

            slot = self.cmb_slot.currentText()

            date_from, date_to = (
                self.get_date_range()
            )

            if not model:
                return

            headers = (
                self.db.get_model_daily_headers()
            )

            data, total_fail, total_yield = (
                self.db.get_model_daily_summary(
                    model=model,
                    date_from=date_from,
                    date_to=date_to,
                    eqp=eqp,
                    handler=handler,
                    zone=zone,
                    slot=slot
                )
            )

            self.model_daily_title.setText(
                f"Model Daily Summary | Model: {model} & Time: {date_from} - {date_to} & EQP: {eqp} & Handler: {handler} & Zone: {zone} | Slot : {slot}"
            )

            self.model_daily_table.setModel(
                TableModel(
                    data,
                    headers,
                    highlight_errors=True
                )
            )


            self.model_daily_table.resizeColumnsToContents()

            self.model_daily_table.resizeRowsToContents()

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "LOAD MODEL DAILY ERROR:",
                repr(e)
            )
    ####BIEU DO CHO TUNG MODEL
    def load_model_daily_chart(self):

        try:

            model = self.cmb_model.currentText()

            eqp = self.cmb_eqp.currentText()

            handler = self.cmb_handler.currentText()

            zone = self.cmb_zone.currentText()

            slot = self.cmb_slot.currentText()

            date_from, date_to = (
                self.get_date_range()
            )
            self.model_daily_chart_title.setText(
                f"Model Daily Summary | Model: {model} & Time: {date_from} - {date_to} & EQP: {eqp} & Handler: {handler} & Zone: {zone} | Slot : {slot}"
            )

            selected_scraps = (
                self.get_selected_scrap_codes()
            )

            dates, yields, scrap_series = (
                self.db.get_model_daily_chart_data(
                    model=model,
                    date_from=date_from,
                    date_to=date_to,
                    eqp=eqp,
                    handler=handler,
                    zone=zone,
                    slot=slot,
                    selected_scraps=selected_scraps
                )
            )

            self.model_daily_chart.update_chart(
                dates,
                yields,
                scrap_series
            )

        except Exception as e:

            import traceback

            traceback.print_exc()

            print(
                "LOAD MODEL DAILY CHART ERROR:",
                repr(e)
            )

    #####================QUẢN LÝ DATABASE
    def create_database_page(self):

        layout = QVBoxLayout()

        self.create_database_filter(layout)

        self.create_database_table(layout)

        self.database_page.setLayout(
            layout
        )

        self.load_database_table()

    def create_database_filter(
            self,
            parent_layout
    ):

        top_layout = QHBoxLayout()

        self.txt_search_date = QLineEdit()
        self.txt_search_date.setFixedHeight(32)
        self.txt_search_date.setPlaceholderText(
            "Input File Date...20260501"
        )
        self.txt_search_date.setFixedHeight(32)

        self.btn_search_date = QPushButton(
            "Search"
        )
        self.btn_search_date.setFixedHeight(32)
        self.btn_search_date.setFixedWidth(160)
        self.btn_search_date.setStyleSheet("""
                            QPushButton {
                                background-color: #0078D7;
                                color: white;
                                border: none;
                                border-radius: 5px;
                                padding: 5px;
                            }
                            QPushButton:hover {
                                background-color: #1E90FF;
                            }
                        """)

        self.btn_refresh_date = QPushButton(
            "Refresh"
        )
        self.btn_refresh_date.setFixedHeight(32)
        self.btn_refresh_date.setFixedWidth(160)
        self.btn_refresh_date.setStyleSheet("""
                            QPushButton {
                                background-color: #0078D7;
                                color: white;
                                border: none;
                                border-radius: 5px;
                                padding: 5px;
                            }
                            QPushButton:hover {
                                background-color: #1E90FF;
                            }
                        """)


        self.btn_delete_date = QPushButton(
            "Delete Selected"
        )
        self.btn_delete_date.setFixedHeight(32)
        self.btn_delete_date.setFixedWidth(160)
        self.btn_delete_date.setStyleSheet("""
                            QPushButton {
                                background-color: #0078D7;
                                color: white;
                                border: none;
                                border-radius: 5px;
                                padding: 5px;
                            }
                            QPushButton:hover {
                                background-color: #1E90FF;
                            }
                        """)

        top_layout.addWidget(
            self.txt_search_date
        )

        top_layout.addWidget(
            self.btn_search_date
        )

        top_layout.addWidget(
            self.btn_refresh_date
        )

        top_layout.addStretch()

        top_layout.addWidget(
            self.btn_delete_date
        )

        parent_layout.addLayout(
            top_layout
        )

        self.btn_search_date.clicked.connect(
            self.search_database_date
        )

        self.btn_refresh_date.clicked.connect(
            self.load_database_table
        )

        self.btn_delete_date.clicked.connect(
            self.delete_selected_dates
        )

    def create_database_table(
            self,
            parent_layout
    ):

        self.database_table = QTableWidget()
        self.database_table.setFixedWidth(800)
        self.database_table.setColumnCount(4)

        self.database_table.setHorizontalHeaderLabels([
            "",
            "File Date",
            "Total Lot ID",
            "Total Qty"
        ])

        self.database_table.horizontalHeader().setStretchLastSection(
            True
        )

        parent_layout.addWidget(
            self.database_table
        )

    def load_database_table(self):

        df = self.db.get_date_summary()

        self.populate_database_table(df)

    def populate_database_table(
            self,
            df
    ):

        self.database_table.setRowCount(
            len(df)
        )

        for row, (_, data) in enumerate(
                df.iterrows()
        ):
            checkbox = QTableWidgetItem()

            checkbox.setFlags(
                Qt.ItemIsUserCheckable |
                Qt.ItemIsEnabled
            )

            checkbox.setCheckState(
                Qt.Unchecked
            )

            self.database_table.setItem(
                row,
                0,
                checkbox
            )

            self.database_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(data["File_Date"])
                )
            )

            self.database_table.setItem(
                row,
                2,
                QTableWidgetItem(
                    f"{int(data['Total_Lots']):,}"
                )
            )

            self.database_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    f"{int(data['Total_Qty']):,}"
                )
            )

    def search_database_date(self):

        date = (
            self.txt_search_date
            .text()
            .strip()
        )

        if not date:
            self.load_database_table()

            return

        df = self.db.search_date_summary(
            date
        )

        if df.empty:
            QMessageBox.information(
                self,
                "Info",
                "File Date not found."
            )

            return

        self.populate_database_table(
            df
        )

    def get_selected_dates(self):

        dates = []

        for row in range(
                self.database_table.rowCount()
        ):

            item = self.database_table.item(
                row,
                0
            )

            if (
                    item and
                    item.checkState()
                    == Qt.Checked
            ):
                dates.append(
                    self.database_table.item(
                        row,
                        1
                    ).text()
                )

        return dates

    def delete_selected_dates(self):

        dates = self.get_selected_dates()

        if not dates:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select date."
            )

            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            (
                f"Delete all data "
                f"for {len(dates)} date(s)?"
            ),
            QMessageBox.Yes |
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        self.db.delete_dates(
            dates
        )

        QMessageBox.information(
            self,
            "Success",
            "Delete completed."
        )

        self.load_database_table()
